# -*- coding: utf-8 -*-
"""ABAP-F.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NBmNSNM5_4DQe-6oFaiK8zMQcqCVAMgh
"""

import streamlit as st
import pandas as pd

# Inicializar las tablas vacías en el estado de la sesión
if 'buchungen' not in st.session_state:
    st.session_state['buchungen'] = pd.DataFrame(columns=['BELNR', 'BUKRS', 'GJAHR', 'KONTO', 'Betrag', 'SOLL', 'HABEN'])

if 'catalogo_sat' not in st.session_state:
    st.session_state['catalogo_sat'] = pd.DataFrame(columns=['CUENTA', 'DESCRIPCION', 'TIPO'])

# Función para procesar los comandos ABAP con términos SAP FI
def verarbeite_abap_befehl(befehl):
    befehl = befehl.strip().upper()
    if befehl.startswith("SELECT"):
        teile = befehl.split("FROM")
        felder = teile[0].replace("SELECT", "").strip()
        tabelle = teile[1].strip()

        if tabelle == "BUCHUNGEN":
            if "WHERE" in befehl:
                bedingung = befehl.split("WHERE")[1].strip()
                if "BELNR" in bedingung:
                    belnr = bedingung.split("=")[1].strip().replace("'", "")
                    ergebnis = st.session_state['buchungen'][st.session_state['buchungen']['BELNR'] == belnr]
                elif "BUKRS" in bedingung:
                    bukrs = bedingung.split("=")[1].strip().replace("'", "")
                    ergebnis = st.session_state['buchungen'][st.session_state['buchungen']['BUKRS'] == bukrs]
                elif "GJAHR" in bedingung:
                    gjahr = bedingung.split("=")[1].strip().replace("'", "")
                    ergebnis = st.session_state['buchungen'][st.session_state['buchungen']['GJAHR'] == gjahr]
                elif "KONTO" in bedingung:
                    konto = bedingung.split("=")[1].strip().replace("'", "")
                    ergebnis = st.session_state['buchungen'][st.session_state['buchungen']['KONTO'] == konto]
                else:
                    ergebnis = pd.DataFrame()  # No encuentra el campo en la condición
            else:
                ergebnis = st.session_state['buchungen']  # Si no hay WHERE, devuelve toda la tabla
            return ergebnis

    return pd.DataFrame()  # Si no es un comando SELECT válido

# Función para agregar una nueva póliza a la tabla
def add_buchung(belnr, bukrs, gjahr, konto, betrag, soll, haben):
    new_row = pd.DataFrame({
        'BELNR': [belnr],
        'BUKRS': [bukrs],
        'GJAHR': [gjahr],
        'KONTO': [konto],
        'Betrag': [betrag],
        'SOLL': [soll],
        'HABEN': [haben]
    })
    st.session_state['buchungen'] = pd.concat([st.session_state['buchungen'], new_row], ignore_index=True)

# Función para agregar cuentas al catálogo del SAT
def add_cuenta_sat(cuenta, descripcion, tipo):
    new_row = pd.DataFrame({
        'CUENTA': [cuenta],
        'DESCRIPCION': [descripcion],
        'TIPO': [tipo]
    })
    st.session_state['catalogo_sat'] = pd.concat([st.session_state['catalogo_sat'], new_row], ignore_index=True)

# Función para generar el Balance General
def balance_general():
    activos = st.session_state['buchungen'][st.session_state['buchungen']['KONTO'].isin([])]['Betrag'].sum()  # No hay cuentas precargadas
    pasivos = st.session_state['buchungen'][st.session_state['buchungen']['KONTO'].isin([])]['Betrag'].sum()  # No hay cuentas precargadas
    capital = st.session_state['buchungen'][st.session_state['buchungen']['KONTO'].isin([])]['Betrag'].sum()  # No hay cuentas precargadas

    return pd.DataFrame({
        'Activo': [activos],
        'Pasivo': [pasivos],
        'Capital': [capital],
        'Total': [activos - pasivos]
    })

# Función para generar el Estado de Resultados
def estado_resultados():
    ingresos = st.session_state['buchungen'][st.session_state['buchungen']['KONTO'].isin([])]['Betrag'].sum()  # No hay cuentas precargadas
    egresos = st.session_state['buchungen'][st.session_state['buchungen']['KONTO'].isin([])]['Betrag'].sum()  # No hay cuentas precargadas

    resultado = ingresos - egresos
    return pd.DataFrame({
        'Ingresos': [ingresos],
        'Egresos': [egresos],
        'Resultado Neto': [resultado]
    })

# Interfaz de Streamlit
st.title("SAP ABAP Befehlsimulator y Generación de Reportes Contables")

# Ingresar comando ABAP
abap_befehl = st.text_area("Geben Sie Ihren ABAP-Befehl ein", "SELECT * FROM buchungen WHERE BELNR = '1001'")

# Formulario para agregar nuevas pólizas
st.subheader("Neue Buchung Hinzufügen (Agregar nueva póliza)")
with st.form(key="add_buchung_form"):
    belnr = st.text_input("BELNR (Número de documento)")
    bukrs = st.text_input("BUKRS (Sociedad)")
    gjahr = st.text_input("GJAHR (Año fiscal)")
    konto = st.text_input("KONTO (Cuenta)")
    betrag = st.number_input("Betrag (Monto)", min_value=0.0)
    soll = st.number_input("SOLL (Debe)", min_value=0.0)
    haben = st.number_input("HABEN (Haber)", min_value=0.0)

    submit_button = st.form_submit_button(label="Póliza Añadir")

    if submit_button:
        if belnr and bukrs and gjahr and konto:
            add_buchung(belnr, bukrs, gjahr, konto, betrag, soll, haben)
            st.success("Póliza agregada exitosamente.")
        else:
            st.warning("Por favor, complete todos los campos.")

# Formulario para agregar cuentas al catálogo del SAT
st.subheader("Agregar Cuenta al Catálogo del SAT")
with st.form(key="add_cuenta_form"):
    cuenta = st.text_input("CUENTA (Número de cuenta)")
    descripcion = st.text_input("DESCRIPCIÓN (Descripción de la cuenta)")
    tipo = st.selectbox("TIPO (Tipo de cuenta)", ["Activo", "Pasivo", "Capital", "Ingreso", "Egreso"])

    submit_button_cuenta = st.form_submit_button(label="Agregar Cuenta")

    if submit_button_cuenta:
        if cuenta and descripcion and tipo:
            add_cuenta_sat(cuenta, descripcion, tipo)
            st.success("Cuenta agregada al catálogo del SAT exitosamente.")
        else:
            st.warning("Por favor, complete todos los campos.")

# Generación de Reportes
st.subheader("Generar Reportes Contables")

# Botón para generar el Balance General
if st.button("Generar Balance General"):
    balance = balance_general()
    st.write("### Balance General:")
    st.dataframe(balance)

# Botón para generar el Estado de Resultados
if st.button("Generar Estado de Resultados"):
    estado = estado_resultados()
    st.write("### Estado de Resultados:")
    st.dataframe(estado)

# Procesar el comando ABAP
if st.button("Befehl Ausführen (Ejecutar Comando)"):
    if abap_befehl:
        # Procesar el comando ABAP y mostrar el resultado
        ergebnis = verarbeite_abap_befehl(abap_befehl)
        if not ergebnis.empty:
            st.write("### Ergebnis der Abfrage:")
            st.dataframe(ergebnis)
        else:
            st.warning("Es wurden keine Ergebnisse für den eingegebenen Befehl gefunden.")