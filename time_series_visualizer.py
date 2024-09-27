import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

# Registrar conversores do Matplotlib
register_matplotlib_converters()

# Importar dados (certifique-se de que o arquivo está no mesmo diretório)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=['date'])

# Limpar dados
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Desenhar gráfico de linha
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Salvar imagem e retornar fig
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copiar e modificar os dados para o gráfico de barras mensal
    df_bar = df.resample('M').mean()  # Usar 'M' para a média do final do mês
    df_bar_plot = df_bar.pivot_table(values='value', index=df_bar.index.year, columns=df_bar.index.month)

    # Desenhar gráfico de barras
    fig = df_bar_plot.plot(kind='bar', figsize=(12, 8), width=0.8).figure
    plt.title('Average Daily Page Views per Month')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    
    # Definir o rótulo da legenda para os meses
    plt.legend(title='Months', labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])

    # Salvar imagem e retornar fig
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Preparar dados para box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Desenhar box plots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
    
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=months)
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    plt.tight_layout()

    # Salvar imagem e retornar fig
    fig.savefig('box_plot.png')
    return fig

# Executar as funções para gerar os gráficos
draw_line_plot()
draw_bar_plot()
draw_box_plot()
