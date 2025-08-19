import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def create_visualizations(df):
    """Cria visualizações para o dashboard"""
    if df.empty:
        return None
    
    visualizations = {}
    
    # Gráfico de pizza - Funcionários por departamento
    dept_count = df['departamento'].value_counts()
    visualizations['dept_pie'] = px.pie(
        values=dept_count.values,
        names=dept_count.index,
        title="Distribuição de Funcionários por Departamento"
    )
    
    # Gráfico de barras - Salários por departamento
    dept_salary = df.groupby('departamento')['salario'].mean().sort_values(ascending=False)
    visualizations['dept_salary_bar'] = px.bar(
        x=dept_salary.index,
        y=dept_salary.values,
        title="Salário Médio por Departamento",
        labels={'x': 'Departamento', 'y': 'Salário Médio (R$)'}
    )
    
    # Histograma - Distribuição de salários
    visualizations['salary_hist'] = px.histogram(
        df,
        x='salario',
        nbins=20,
        title="Distribuição de Salários",
        labels={'salario': 'Salário (R$)', 'count': 'Quantidade'}
    )
    
    # Box plot - Distribuição salarial por departamento
    visualizations['salary_box'] = px.box(
        df,
        x='departamento',
        y='salario',
        title="Variação Salarial por Departamento"
    )
    
    # Gráfico de linha - Contratações ao longo do tempo
    if 'data_admissao' in df.columns:
        df_temp = df.copy()
        df_temp['data_admissao'] = pd.to_datetime(df_temp['data_admissao'])
        monthly_hires = df_temp.groupby(df_temp['data_admissao'].dt.to_period('M')).size()
        
        visualizations['hiring_trend'] = px.line(
            x=monthly_hires.index.astype(str),
            y=monthly_hires.values,
            title="Tendência de Contratações",
            labels={'x': 'Mês', 'y': 'Número de Contratações'}
        )
    
    # Gráfico de barras - Top 10 salários
    top_salaries = df.nlargest(10, 'salario')
    visualizations['top_salaries'] = px.bar(
        top_salaries,
        x='nome',
        y='salario',
        title="Top 10 Maiores Salários",
        labels={'nome': 'Nome', 'salario': 'Salário (R$)'}
    )
    
    return visualizations

def create_department_analysis(df):
    """Cria análises específicas por departamento"""
    if df.empty:
        return None
    
    analysis = {}
    
    # Estatísticas por departamento
    dept_stats = df.groupby('departamento').agg({
        'nome': 'count',
        'salario': ['mean', 'sum', 'min', 'max']
    }).round(2)
    
    dept_stats.columns = ['Total_Funcionários', 'Salário_Médio', 'Folha_Total', 'Menor_Salário', 'Maior_Salário']
    analysis['statistics'] = dept_stats
    
    # Gráfico de custo total por departamento
    dept_cost = df.groupby('departamento')['salario'].sum().sort_values(ascending=False)
    analysis['cost_chart'] = px.bar(
        x=dept_cost.index,
        y=dept_cost.values,
        title="Custo Total por Departamento",
        labels={'x': 'Departamento', 'y': 'Custo Total (R$)'}
    )
    
    # Gráfico de funcionários por departamento
    dept_count = df['departamento'].value_counts()
    analysis['count_chart'] = px.bar(
        x=dept_count.index,
        y=dept_count.values,
        title="Número de Funcionários por Departamento",
        labels={'x': 'Departamento', 'y': 'Número de Funcionários'}
    )
    
    return analysis

def create_salary_analysis(df):
    """Cria análises específicas de salários"""
    if df.empty:
        return None
    
    analysis = {}
    
    # Estatísticas gerais
    analysis['total_payroll'] = df['salario'].sum()
    analysis['avg_salary'] = df['salario'].mean()
    analysis['median_salary'] = df['salario'].median()
    analysis['salary_std'] = df['salario'].std()
    
    # Quartis
    analysis['q1'] = df['salario'].quantile(0.25)
    analysis['q3'] = df['salario'].quantile(0.75)
    
    # Funcionários por faixa salarial
    salary_ranges = pd.cut(
        df['salario'], 
        bins=[0, 3000, 5000, 8000, 12000, float('inf')],
        labels=['Até R$3.000', 'R$3.001-5.000', 'R$5.001-8.000', 'R$8.001-12.000', 'Acima de R$12.000']
    )
    
    range_counts = pd.Series(salary_ranges).value_counts().sort_index()
    analysis['salary_ranges_chart'] = px.bar(
        x=range_counts.index,
        y=range_counts.values,
        title="Funcionários por Faixa Salarial",
        labels={'x': 'Faixa Salarial', 'y': 'Número de Funcionários'}
    )
    
    return analysis

def create_growth_analysis(df):
    """Cria análises de crescimento da empresa"""
    if df.empty or 'data_admissao' not in df.columns:
        return None
    
    analysis = {}
    
    # Converter datas
    df_temp = df.copy()
    df_temp['data_admissao'] = pd.to_datetime(df_temp['data_admissao'])
    
    # Contratações por mês
    monthly_hires = df_temp.groupby(df_temp['data_admissao'].dt.to_period('M')).size()
    analysis['monthly_hires'] = px.line(
        x=monthly_hires.index.astype(str),
        y=monthly_hires.values,
        title="Contratações Mensais",
        labels={'x': 'Mês', 'y': 'Contratações'}
    )
    
    # Crescimento cumulativo
    df_sorted = df_temp.sort_values('data_admissao')
    df_sorted['employees_cumulative'] = range(1, len(df_sorted) + 1)
    
    analysis['cumulative_growth'] = px.line(
        df_sorted,
        x='data_admissao',
        y='employees_cumulative',
        title="Crescimento Cumulativo de Funcionários",
        labels={'data_admissao': 'Data', 'employees_cumulative': 'Total de Funcionários'}
    )
    
    # Taxa de crescimento mensal
    monthly_growth = monthly_hires.pct_change().fillna(0) * 100
    analysis['growth_rate'] = px.bar(
        x=monthly_growth.index.astype(str),
        y=monthly_growth.values,
        title="Taxa de Crescimento Mensal (%)",
        labels={'x': 'Mês', 'y': 'Taxa de Crescimento (%)'}
    )
    
    return analysis

def create_status_analysis(df):
    """Cria análises por status dos funcionários"""
    if df.empty or 'status' not in df.columns:
        return None
    
    analysis = {}
    
    # Distribuição por status
    status_count = df['status'].value_counts()
    analysis['status_pie'] = px.pie(
        values=status_count.values,
        names=status_count.index,
        title="Distribuição por Status"
    )
    
    # Status por departamento
    status_dept = df.groupby(['departamento', 'status']).size().unstack(fill_value=0)
    analysis['status_by_dept'] = px.bar(
        status_dept,
        title="Status por Departamento",
        labels={'value': 'Número de Funcionários', 'index': 'Departamento'}
    )
    
    return analysis
