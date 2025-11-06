import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

class MetricasTesting:
    """
    Clase para gestionar métricas de calidad y testing del sistema de reservas.
    Calcula indicadores, tendencias y genera dashboards visuales.
    """

    def __init__(self, dataset_path='data/dataset_defectos.csv'):
        self.dataset_path = dataset_path
        self.df = None
        self.indicadores = {}

    def cargar_datos(self):
        """Carga el dataset de defectos desde un CSV."""
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"No se encontró el archivo: {self.dataset_path}")
        self.df = pd.read_csv(self.dataset_path)
        print(f"✅ Datos cargados: {len(self.df)} registros")

    def calcular_indicadores(self):
        """Calcula 8 métricas principales de control de calidad."""
        if self.df is None:
            raise ValueError("Debe cargar los datos antes de calcular indicadores.")

        total_defectos = len(self.df)
        defectos_abiertos = len(self.df[self.df['Estado'] == 'Abierto'])
        defectos_cerrados = len(self.df[self.df['Estado'] == 'Cerrado'])
        tasa_cierre = round((defectos_cerrados / total_defectos) * 100, 2)

        severidad_prom = self.df['Severidad'].mean()
        ocurrencia_prom = self.df['Ocurrencia'].mean()
        deteccion_prom = self.df['Deteccion'].mean()
        rpn_prom = self.df['RPN'].mean()

        self.indicadores = {
            "Total defectos": total_defectos,
            "Defectos abiertos": defectos_abiertos,
            "Defectos cerrados": defectos_cerrados,
            "Tasa de cierre (%)": tasa_cierre,
            "Severidad promedio": round(severidad_prom, 2),
            "Ocurrencia promedio": round(ocurrencia_prom, 2),
            "Detección promedio": round(deteccion_prom, 2),
            "RPN promedio": round(rpn_prom, 2)
        }

        print("📊 Indicadores calculados correctamente.")
        return self.indicadores

    def detectar_tendencia(self):
        """Analiza tendencia de defectos abiertos y cerrados por día."""
        if 'Fecha' not in self.df.columns:
            print("⚠️ No hay columna 'Fecha' para análisis temporal.")
            return None

        tendencia = self.df.groupby(['Fecha', 'Estado']).size().unstack(fill_value=0)
        print("📈 Tendencia de defectos generada correctamente.")
        return tendencia

    def generar_dashboard(self, nombre_archivo='dashboard_dia.html'):
        """Genera un dashboard visual (PNG + HTML) de los indicadores."""
        if not self.indicadores:
            raise ValueError("Debe calcular los indicadores antes de generar el dashboard.")

        etiquetas = list(self.indicadores.keys())
        valores = list(self.indicadores.values())

        plt.figure(figsize=(10, 5))
        plt.barh(etiquetas, valores, color='teal')
        plt.title('Indicadores de Métricas de Testing')
        plt.xlabel('Valor')
        plt.tight_layout()

        # Crear carpeta si no existe
        os.makedirs("dashboard_snapshots", exist_ok=True)

        nombre_png = nombre_archivo.replace(".html", ".png")
        ruta_png = os.path.join("dashboard_snapshots", nombre_png)
        plt.savefig(ruta_png)
        plt.close()

        # Generar HTML simple
        html_content = f"""
        <html>
        <head><title>Dashboard Testing</title></head>
        <body>
        <h2>📊 Dashboard de Métricas ({datetime.now().strftime('%Y-%m-%d')})</h2>
        <img src="{nombre_png}" alt="Dashboard">
        <h3>Indicadores</h3>
        <ul>
        {''.join([f"<li>{k}: {v}</li>" for k, v in self.indicadores.items()])}
        </ul>
        </body>
        </html>
        """
        ruta_html = os.path.join("dashboard_snapshots", nombre_archivo)
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ Dashboard generado: {ruta_html}")
        return ruta_html
