import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('ventas_tienda.csv')

# -- Gráfico 1: Ventas por producto 
ventas_prod = df.groupby('producto')['cantidad'].sum()

ax1 = ventas_prod.plot(kind='bar', color='#A7C7E7', edgecolor='black', figsize=(8,5), title='Ventas por Producto')
ax1.set_xlabel('Producto'), ax1.set_ylabel('Cantidad Vendida'), ax1.grid(axis='y', linestyle='--', alpha=0.7)
for p in ax1.patches:
    ax1.annotate(str(int(p.get_height())), (p.get_x() + p.get_width() / 2, p.get_height() + 2), ha='center')
plt.figtext(0.5, 0.01, "Ventas totales por producto durante 6 meses.", ha='center', fontsize=9, style='italic')
plt.tight_layout(); plt.show()

# -- Gráfico 2: Ventas por mes y producto con cuadro de texto externo
orden_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']
df['mes'] = pd.Categorical(df['mes'], categories=orden_meses, ordered=True)

ventas_mes = df.groupby(['mes', 'producto'])['cantidad'].sum().unstack()
ventas_tot_mes = df.groupby('mes')['cantidad'].sum().reindex(orden_meses)

fig, ax2 = plt.subplots(figsize=(10,5))
ventas_mes.plot(marker='o', ax=ax2, title='Ventas por Mes y Producto', color=['#FFB6B9', '#FFDAC1', '#E2F0CB', '#B5EAD7', '#C7CEEA'])
ax2.set_xlabel('Mes'), ax2.set_ylabel('Cantidad Vendida')

plt.subplots_adjust(right=0.7)

# Cuadro de texto con unidades por mes
text_content = "Unidades por mes:\n" + "\n".join([f"{mes}: {int(cant)}" for mes, cant in ventas_tot_mes.items()])
plt.figtext(0.72, 0.85, text_content, bbox=dict(facecolor='white', alpha=0.8, boxstyle='round'), 
            fontsize=9, verticalalignment='top')

for col in ventas_mes.columns:
    for i, val in enumerate(ventas_mes[col]):
        ax2.text(i, val + 1, int(val), ha='center', fontsize=8)
ax2.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Producto', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.figtext(0.5, 0.01, "Ventas mensuales de cada producto.", ha='center', fontsize=9, style='italic')
plt.tight_layout(); plt.show()

#Tabla resumen: Ingresos por producto con promedios
if 'precio_unitario' in df.columns:
    df['ingresos'] = df['cantidad'] * df['precio_unitario']
    ingresos = df.groupby('producto')['ingresos'].sum().sort_values(ascending=False)
    resumen = pd.DataFrame({'Producto': ingresos.index, 'Ingresos Totales': ingresos.map("${:,.2f}".format)})
    
    # Calcular promedios
    promedios = (df.groupby('producto')['cantidad'].sum() / 6).round(2)
    prom_df = pd.DataFrame({'Producto': promedios.index, 'Promedio Mensual': promedios.values})

    # Crear figura con dos tablas
    fig, (ax, ax_prom) = plt.subplots(2, 1, figsize=(8, 6))
    fig.suptitle('Resumen Financiero y de Ventas', fontsize=14, fontweight='bold')
    
    # Tabla de ingresos
    ax.axis('off')
    ax.table(cellText=resumen.values, colLabels=resumen.columns, loc='center', cellLoc='center').scale(1, 1.4)
    ax.set_title('Ingresos por Producto', fontsize=12, pad=10)
    
    # Tabla de promedios
    ax_prom.axis('off')
    ax_prom.table(cellText=prom_df.values, colLabels=prom_df.columns, loc='center', cellLoc='center').scale(1, 1.4)
    ax_prom.set_title('Promedio Mensual por Producto', fontsize=12, pad=10)
    
    plt.figtext(0.5, 0.01, "Resumen financiero y de ventas promedio durante 6 meses.", ha='center', fontsize=9, style='italic')
    plt.tight_layout(); plt.subplots_adjust(hspace=0.5)
    plt.show()
else:
    print("Falta la columna 'precio_unitario'.")

