import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, BatchNormalization
from keras.layers import Dropout, Bidirectional
from keras.optimizers import Adam
from keras.callbacks import ReduceLROnPlateau, EarlyStopping
from keras.regularizers import l2
from time import time
import optuna


# Funció per crear el conjunt de dades amb finestres temporals
def crear_conjunt_dades(dades, passos_temps=1):
    X, y = [], []
    for i in range(len(dades) - passos_temps):
        X.append(dades[i:(i + passos_temps)])
        y.append(dades[i + passos_temps])
    return np.array(X), np.array(y)


# Funció per carregar les dades del fitxer Excel
def carregar_dades(file_path=None, data_pos_col=True,
                   llindar_zeros=0.3, passos_temps=7, n_particio=440):

    dades = pd.read_excel(file_path, header=None)

    # Configurar la primera fila com a capçalera
    df = pd.DataFrame(dades)
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])
    df = df.reset_index(drop=True)

    # Convertir les columnes a datetime excepte la primera columna
    df.columns = ['Article'] + [pd.to_datetime(col) for col in df.columns[1:]]
    df.set_index('Article', inplace=True)
    if data_pos_col:
        df = df.T
    df.index = pd.to_datetime(df.index)
    if llindar_zeros is not None:
        # Filtrar productes amb molts zeros
        zero_counts_per_column = 0.3 > (df == 0).sum() / len(df)
        df = df.loc[:, zero_counts_per_column]

    # Carregar les dades
    dades = df.values

    # Convertir les dades a float64 (necessari per a LSTM)
    dades = dades.astype(np.float64)

    # Normalitzar les dades
    escalador = MinMaxScaler(feature_range=(0, 1))
    dades = escalador.fit_transform(dades)

    n = len(dades)
    if passos_temps * 2 > len(dades):
        dades_train = dades[:passos_temps + 31, :]
        dades_test = dades[n-passos_temps-30:, :]
    else:
        dades_train = dades[:n-n_particio + 1, :]
        dades_test = dades[n-n_particio:, :]

    # Crear el conjunt de dades amb finestres temporals
    X, y = crear_conjunt_dades(dades_train, passos_temps)
    X_test, y_test = crear_conjunt_dades(dades_test, passos_temps)

    # Reestructurar X per adaptar-lo a la forma d'entrada de LSTM
    X = np.reshape(X, (X.shape[0], passos_temps, X.shape[2]))
    X_test = np.reshape(X_test,
                        (X_test.shape[0], passos_temps, X_test.shape[2]))

    return X, y, X_test, y_test, escalador


# Funció per crear el model LSTM
def crear_model(CAPES, LR, LAMBD, DP, DP_dense,
                passos_temps, característiques):
    model = Sequential()
    for tipus_capa, n_cel·les in CAPES:
        if tipus_capa == "Bi_LSTM":
            model.add(Bidirectional(LSTM(units=n_cel·les, activation='tanh',
                                         recurrent_activation='hard_sigmoid',
                                    kernel_regularizer=l2(LAMBD),
                                    recurrent_regularizer=l2(LAMBD),
                                    dropout=DP, return_sequences=True,
                                    input_shape=(
                                        passos_temps, característiques))))
            model.add(BatchNormalization())
            model.add(Dropout(DP))
        elif tipus_capa == "Last_Bi_LSTM":
            model.add(Bidirectional(LSTM(units=n_cel·les,
                                         activation='tanh',
                                         recurrent_activation='hard_sigmoid',
                                    kernel_regularizer=l2(LAMBD),
                                    recurrent_regularizer=l2(LAMBD),
                                    dropout=DP, input_shape=(
                                        passos_temps, característiques))))
            model.add(BatchNormalization())
            model.add(Dropout(DP))
        elif tipus_capa == "Dense":
            model.add(Dense(units=n_cel·les))
            model.add(Dropout(DP_dense))

    model.add(Dense(units=característiques, activation='sigmoid'))

    model.compile(optimizer=Adam(learning_rate=LR),
                  loss='mean_squared_error', metrics=['accuracy'])
    return model


# Funció per executar el model
def executar_model(model, X, y, LOT=20, EPOCHS=100):
    lr_decay = ReduceLROnPlateau(monitor='loss', patience=3, verbose=1,
                                 factor=0.25, min_lr=1e-8)
    early_stop = EarlyStopping(monitor='val_loss', patience=10, verbose=1,
                               restore_best_weights=True)

    start_time = time()
    history = model.fit(X, y, epochs=EPOCHS, batch_size=LOT,
                        validation_split=0.2, shuffle=True, verbose=1,
                        callbacks=[lr_decay, early_stop])

    print(f"Entrenament completat en {time() - start_time} segons.")
    return model, history


# Funció per mostrar els resultats del model
def resultats_model(model, history, escalador, X_test, y_test, LOT=20):
    test_loss, test_acc = model.evaluate(X_test, y_test, batch_size=LOT)
    print(f"Pèrdua de test: {test_loss}, Precisió del test: {test_acc}")

    train_loss = history.history['loss']
    val_loss = history.history['val_loss']

    plt.figure(figsize=(12, 6))
    plt.plot(train_loss, label='Pèrdua Entrenament')
    plt.plot(val_loss, label='Pèrdua Validació')
    plt.title('Evolució de la pèrdua durant l\'entrenament')
    plt.xlabel('Èpoques')
    plt.ylabel('Pèrdua')
    plt.legend()

    prediccions = model.predict(X_test)

    # Invertir la normalització
    prediccions = escalador.inverse_transform(prediccions)
    y_test = escalador.inverse_transform(y_test)

    num_productes = min(6, prediccions.shape[1])
    plt.close('all')
    plt.figure(figsize=(16, 10))
    for i in range(num_productes):
        plt.subplot(num_productes, 1, i + 1)
        plt.plot(prediccions[:, i], label=f'Producte {i+1} Previst')
        plt.plot(y_test[:, i], label=f'Producte {i+1} Real')
        plt.title(f'Producte {i+1} Prevenció vs Vendes Reals')
        plt.legend()

    plt.tight_layout()
    return test_loss, test_acc


# Funció per guardar el model
def guardar_model(model, path):
    model.save(path)
    print("Model guardat a: " + path)


# Funció objectiu per a l'optimització amb Optuna
def objectiu(trial):
    passos_temps = trial.suggest_categorical('passos_temps', [30])
    LR = trial.suggest_loguniform('LR', 1e-6, 5*1e-2)
    LAMBD = trial.suggest_loguniform('LAMBD', 1e-6, 1e-4)
    DP = trial.suggest_uniform('DP', 0.1, 0.3)
    DP_dense = trial.suggest_uniform('DP_dense', 0.1, 0.3)
    lot = trial.suggest_int('LOT', 2, 20)
    epochs = trial.suggest_int('EPOCHS', 50, 400)

    # Carregar les dades
    X, y, X_test, y_test, escalador = carregar_dades(passos_temps=passos_temps)

    # Definir les capes del model
    CAPES = [('Last_Bi_LSTM',
              trial.suggest_int('Last_Bi_LSTM_units', 100, 200)),
             ('Dense', trial.suggest_int('Dense_units', 100, 200))]

    # Crear el model
    model = crear_model(CAPES=CAPES, LR=LR, LAMBD=LAMBD, DP=DP,
                        DP_dense=DP_dense, passos_temps=passos_temps,
                        característiques=X.shape[2])

    # Executar el model
    model, history = executar_model(model, X, y, LOT=lot, EPOCHS=epochs)

    # Obtenir resultats
    test_loss, test_acc = resultats_model(model, history, escalador,
                                          X_test, y_test, LOT=lot)

    # Retornar la pèrdua de test per optimitzar-la
    return -test_loss  # Optimitzem per la pèrdua


# Configurar l'estudi amb Optuna
estudi = optuna.create_study(direction='maximize')
estudi.optimize(objectiu, n_trials=500)

# Guardar els millors models
millors_proves = sorted(estudi.trials, key=lambda t: t.value,
                        reverse=True)[:10]

for prova in millors_proves:
    parametres = prova.params
    passos_temps = parametres['passos_temps']
    X, y, X_test, y_test, escalador = carregar_dades(passos_temps=passos_temps)
    CAPES = [('Last_Bi_LSTM', parametres['Last_Bi_LSTM_units']),
             ('Dense', parametres['Dense_units'])]
    model = crear_model(CAPES=CAPES, LR=parametres['LR'],
                        LAMBD=parametres['LAMBD'],
                        DP=parametres['DP'], DP_dense=parametres['DP_dense'],
                        passos_temps=passos_temps, característiques=X.shape[2])
    model, history = executar_model(model, X, y, LOT=parametres['LOT'],
                                    EPOCHS=parametres['EPOCHS'])

    test_loss, acc = resultats_model(model, history, escalador, X_test, y_test,
                                     LOT=parametres['LOT'])
    guardar_model(
        model,
        f"models_auto/{test_loss:.5f}_{passos_temps}_{parametres['LOT']}" +
        f"_{parametres['EPOCHS']}_{parametres['DP_dense']}" +
        f"_{parametres['LAMBD']}" +
        f"_{parametres['DP']}_{parametres['LR']}.keras")

print("Optimització completada. Models principals guardats.")
