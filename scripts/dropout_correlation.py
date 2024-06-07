import pandas as pd
import numpy as np
import hvplot.pandas
import holoviews as hv
from holoviews import opts
import panel as pn
from matplotlib.colors import LinearSegmentedColormap

pn.extension('bokeh')

# Генерация примерных данных для students_info_data
np.random.seed(42)
students_info_data = pd.DataFrame({
    'возраст': np.random.randint(20, 60, 100),
    'опыт_работы': np.random.randint(1, 30, 100),
    'оценка_итог': np.random.uniform(2.0, 5.0, 100),
    'количество_заданий': np.random.randint(10, 100, 100),
    'время_выполнения': np.random.uniform(30, 300, 100)
})

# Создание градиента из большего количества цветов
colors = ["#ff66c4", "#ff66a5", "#ff6685", "#ff6665", "#ff6645", "#ff6625", "#ff6605", "#d357ff", "#a457ff", "#7057ff", "#5170ff", "#5470fe"]

# Функция для построения корреляционной матрицы
def plot_correlation_matrix(data, title):
    correlation_matrix = data.corr()
    correlation_matrix = correlation_matrix.reset_index().melt(id_vars='index')
    
    heatmap = correlation_matrix.hvplot.heatmap(
        x='variable', y='index', C='value', cmap=colors,
        colorbar=True, title=title, clim=(-1, 1)
    ).opts(
        opts.HeatMap(width=800, height=600, tools=['hover'], xrotation=45, colorbar=True)
    )
    return heatmap

# Преобразование данных для построения корреляционной матрицы
correlation_matrix = students_info_data.corr().stack().reset_index()
correlation_matrix.columns = ['Feature 1', 'Feature 2', 'Correlation']

# Создание панели с корреляционной матрицей
correlation_matrix_pane = plot_correlation_matrix(students_info_data, 'Корреляционная матрица признаков')

# Отображение панели
dashboard = pn.Column(
    pn.pane.Markdown("# Корреляционная матрица признаков"),
    correlation_matrix_pane
)

# Запуск панели
pn.serve(dashboard)




