Import streamlit as st

Import pandas as pd

From datetime import datetime



Class SistemaContable:

    Def __init__(self):

        Self.libro_diario = []

        Self.folios = {}

        Self.contador_folios = 1



        Self.catalogo = {

            “CAJA”: {“tipo”: “ACTIVO”, “grupo”: “CORRIENTE”},

            “BANCO”: {“tipo”: “ACTIVO”, “grupo”: “CORRIENTE”},

            “MERCADERIA”: {“tipo”: “ACTIVO”, “grupo”: “CORRIENTE”},

            “IVA CF”: {“tipo”: “ACTIVO”, “grupo”: “CORRIENTE”},

            “CUENTAS POR COBRAR”: {“tipo”: “ACTIVO”, “grupo”: “CORRIENTE”},

            “DOC POR COBRAR”: {“tipo”: “ACTIVO”, “grupo”: “CORRIENTE”},

            “ANTICIPO A PROVEEDORES”: {“tipo”: “ACTIVO”, “grupo”: “CORRIENTE”},

            “IVA A FAVOR”: {“tipo”: “ACTIVO”, “grupo”: “CORRIENTE”},

            “EDIFICIO”: {“tipo”: “ACTIVO”, “grupo”: “NO CORRIENTE”},

            “MUEBLES Y ENSERES”: {“tipo”: “ACTIVO”, “grupo”: “NO CORRIENTE”},

            “VEHICULO”: {“tipo”: “ACTIVO”, “grupo”: “NO CORRIENTE”},

            “GASTOS DE ORGANIZACIÓN”: {“tipo”: “ACTIVO”, “grupo”: “NO CORRIENTE”},

            “CUENTAS POR PAGAR”: {“tipo”: “PASIVO”, “grupo”: “CORRIENTE”},

            “IVA DF”: {“tipo”: “PASIVO”, “grupo”: “CORRIENTE”},

            “IT POR PAGAR”: {“tipo”: “PASIVO”, “grupo”: “CORRIENTE”},

            “IUE POR PAGAR”: {“tipo”: “PASIVO”, “grupo”: “CORRIENTE”},

            “APORTES Y RETENCIONES POR PAGAR”: {“tipo”: “PASIVO”, “grupo”: “CORRIENTE”},

            “AGUINALDO POR PAGAR”: {“tipo”: “PASIVO”, “grupo”: “CORRIENTE”},

            “DOCUMENTOS POR PAGAR”: {“tipo”: “PASIVO”, “grupo”: “NO CORRIENTE”},

            “PROVISION PARA LA INDEMNIZACION”: {“tipo”: “PASIVO”, “grupo”: “NO CORRIENTE”},

            “CAPITAL”: {“tipo”: “PATRIMONIO”, “grupo”: “”},

            “RESULTADO DEL EJERCICIO”: {“tipo”: “PATRIMONIO”, “grupo”: “”},

            “UTILIDAD”: {“tipo”: “PATRIMONIO”, “grupo”: “”},

            “VENTAS”: {“tipo”: “INGRESO”, “grupo”: “”},

            “BONIFICACION SOBRE COMPRAS”: {“tipo”: “INGRESO”, “grupo”: “”},

            “COSTO DE MERCADERIA VENDIDA”: {“tipo”: “EGRESO”, “grupo”: “”},

            “SUELDOS Y SALARIOS”: {“tipo”: “EGRESO”, “grupo”: “”},

            “IT”: {“tipo”: “EGRESO”, “grupo”: “”},

            “GASTO DE CHEQUERA”: {“tipo”: “EGRESO”, “grupo”: “”},

            “CARGAS SOCIALES”: {“tipo”: “EGRESO”, “grupo”: “”},

            “RECARGO SOBRE COMPRAS”: {“tipo”: “EGRESO”, “grupo”: “”},

            “PERDIDAS Y GANANCIAS”: {“tipo”: “TRANSITORIA”, “grupo”: “”}

        }



    Def obtener_folio(self, cuenta):

        If cuenta not in self.folios:

            Self.folios[cuenta] = self.contador_folios

            Self.contador_folios += 1

        Return self.folios[cuenta]



    Def registrar_asiento(self, fecha, glosa, movimientos):

        Asiento_id = len(set(x[“Asiento_ID”] for x in self.libro_diario)) + 1

        If not glosa.lower().strip().startswith(“por”):

            Glosa = “por “ + glosa



        For mov in movimientos:

            Info = self.catalogo.get(mov[“cuenta”], {“tipo”: “OTRO”, “grupo”: “CORRIENTE”})

            Folio = self.obtener_folio(mov[“cuenta”])



            Self.libro_diario.append({

                “Fecha”: fecha,

                “Asiento_ID”: asiento_id,

                “Glosa”: glosa,

                “Ref”: folio,

                “Cuenta”: mov[“cuenta”],

                “Tipo”: info[“tipo”],

                “Grupo”: info[“grupo”],

                “Debe”: float(mov[“debe”]),

                “Haber”: float(mov[“haber”])

            })



    Def obtener_libro_diario_df(self):

        Return pd.DataFrame(self.libro_diario) if self.libro_diario else pd.DataFrame()



St.set_page_config(page_title=”Sistema Contable Web”, layout=”wide”)

St.title(“📱 Sistema Contable v10.2 – Accesible desde tu teléfono”)



If “sistema” not in st.session_state:

    St.session_state.sistema = SistemaContable()



Sistema = st.session_state.sistema



Tab_reg, tab_dia = st.tabs([“📝 Registrar Asiento”, “📚 Libro Diario”])



With tab_reg:

    St.subheader(“Registrar operación”)

    Tipo_op = st.radio(“Tipo de operación”, [“Compra”, “Venta”, “Otro”], horizontal=True)



    Fecha = st.date_input(“Fecha”, value=datetime.today())

    Glosa = st.text_input(“Glosa”, placeholder=”Ej: compra de mercadería”)



    Col1, col2 = st.columns(2)

    With col1:

        Cuenta_debe = st.selectbox(“Cuenta Débito”, sorted(sistema.catalogo.keys()))

        Monto_debe = st.number_input(“Monto Débito”, min_value=0.0, step=10.0, format=”%.2f”)

    With col2:

        Cuenta_haber = st.selectbox(“Cuenta Crédito”, sorted(sistema.catalogo.keys()))

        Monto_haber = st.number_input(“Monto Crédito”, min_value=0.0, step=10.0, format=”%.2f”)



    Movimientos = []

    If tipo_op == “Compra” and cuenta_debe == “MERCADERIA”:

        Iva = monto_debe * 0.13

        Movimientos.append({“cuenta”: “MERCADERIA”, “debe”: monto_debe, “haber”: 0})

        Movimientos.append({“cuenta”: “IVA CF”, “debe”: iva, “haber”: 0})

        Movimientos.append({“cuenta”: cuenta_haber, “debe”: 0, “haber”: monto_debe + iva})

        St.info(f”✅ Se agregó IVA CF: {iva:.2f} (13%)”)



    Elif tipo_op == “Venta” and cuenta_haber == “VENTAS”:

        Iva = monto_haber * 0.13

        It = monto_haber * 0.03

        Total = monto_haber + iva + it



        Movimientos.append({“cuenta”: cuenta_debe, “debe”: total, “haber”: 0})

        Movimientos.append({“cuenta”: “VENTAS”, “debe”: 0, “haber”: monto_haber})

        Movimientos.append({“cuenta”: “IVA DF”, “debe”: 0, “haber”: iva})

        Movimientos.append({“cuenta”: “IT POR PAGAR”, “debe”: 0, “haber”: it})



        St.info(f”✅ Se agregó IVA DF: {iva:.2f} (13%) e IT: {it:.2f} (3%)”)



    Else:

        If monto_debe > 0 or monto_haber > 0:

            If abs(monto_debe – monto_haber) < 0.01:

                Movimientos.append({“cuenta”: cuenta_debe, “debe”: monto_debe, “haber”: 0})

                Movimientos.append({“cuenta”: cuenta_haber, “debe”: 0, “haber”: monto_haber})

            Else:

                St.warning(“⚠️ En operaciones ‘Otro’, Débito y Crédito deben ser iguales.”)



    If st.button(“💾 Guardar Asiento”):

        If not movimientos:

            St.error(“❌ No hay movimientos válidos.”)

        Else:

            Sistema.registrar_asiento(str(fecha), glosa, movimientos)

            St.success(“✅ Asiento guardado correctamente.”)



With tab_dia:

    St.subheader(“Libro Diario”)

    Df = sistema.obtener_libro_diario_df()



    If df.empty:

        St.info(“No hay asientos registrados aún.”)

    Else:

        Df_display = df[[“Fecha”, “Asiento_ID”, “Glosa”, “Cuenta”, “Debe”, “Haber”]].copy()

        Df_display[“Debe”] = df_display[“Debe”].apply(lambda x: f”{x:,.2f}”)

        Df_display[“Haber”] = df_display[“Haber”].apply(lambda x: f”{x:,.2f}”)

        St.dataframe(df_display, use_container_width=True)



