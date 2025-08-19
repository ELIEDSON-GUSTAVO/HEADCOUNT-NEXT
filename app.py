import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import os

# SOLUÇÃO PARA O ERRO removeChild
import streamlit as st
from streamlit import _bottom

# Configuração especial para evitar o erro
st.set_page_config(
    page_title="Sistema de Gestão de Funcionários",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache otimizado para evitar recriação de componentes
@st.cache_resource(show_spinner=False)
def get_data_handler():
    return DataHandler()

# Sua classe DataHandler (se necessário como fallback)
class DataHandler:
    def __init__(self):
        self.data_file = "data/funcionarios.csv"
    
    def load_data(self):
        try:
            return pd.read_csv(self.data_file, sep=";")
        except:
            return pd.DataFrame()
# Importações locais (com fallback)
try:
    from utils.data_handler import DataHandler
    from utils.visualizations import create_visualizations
except ImportError:
    # Fallback caso os módulos não estejam disponíveis
    class DataHandler:
        def __init__(self):
            self.data_file = "data/funcionarios.csv"
        
        def load_data(self):
            try:
                return pd.read_csv(self.data_file, sep=";")
            except:
                return pd.DataFrame()
    
    def create_visualizations():
        return {}

# Configuração de tema customizado
st.markdown("""
<style>
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1E1E1E;
    }
    
    /* Main content area */
    .stApp {
        background-color: #1E1E1E;
    }
    
    /* Metrics styling */
    .metric-container {
        background: linear-gradient(135deg, #2D2D2D 0%, #1E1E1E 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #FF0000;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FF0000 0%, #CC0000 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #CC0000 0%, #990000 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.3);
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #2D2D2D;
        border: 1px solid #FF0000;
        color: #FFFFFF;
    }
    
    /* Headers styling */
    h1, h2, h3 {
        color: #FF0000 !important;
        font-weight: bold;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #2D2D2D;
        border: 1px solid #FF0000;
        color: #FFFFFF;
    }
    
    /* Table styling */
    .stDataFrame {
        background-color: #2D2D2D;
    }
</style>
""", unsafe_allow_html=True)

# Configuração da página
st.set_page_config(
    page_title="Sistema de Gestão de Funcionários",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar o manipulador de dados - CORREÇÃO AQUI
_data_handler = None
def get_data_handler():
    global _data_handler
    if _data_handler is None:
        _data_handler = DataHandler()
    return _data_handler

data_handler = get_data_handler()

# Título principal
st.title("👥 Sistema de Gestão de Funcionários")
st.markdown("---")

# Cache para dados - CORREÇÃO AQUI
@st.cache_data(ttl=300, show_spinner=False)
def load_cached_data():
    return data_handler.load_data()

# Sidebar para navegação
st.sidebar.title("📋 Menu de Navegação")

# Botão de atualização automática
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Atualizar Dados", use_container_width=True, key="refresh_button_unique"):
    st.cache_data.clear()
    st.rerun()

# Carregar dados com cache - CORREÇÃO AQUI
df = load_cached_data()

# Informações em tempo real
if not df.empty:
    st.sidebar.metric("Total de Funcionários", len(df), key="total_func_metric_unique")
    st.sidebar.metric("Folha Salarial", f"R$ {df['salario'].sum():,.2f}", key="folha_metric_unique")
    st.sidebar.metric("Último Update", datetime.now().strftime("%H:%M:%S"), key="update_metric_unique")

st.sidebar.markdown("---")
page = st.sidebar.selectbox(
    "Selecione uma opção:",
    ["🏠 Dashboard", "👤 Funcionários", "📊 Relatórios", "⚙️ Configurações"],
    key="nav_selectbox_unique"
)

# Função para exibir dashboard
def show_dashboard():
    st.header("📊 Dashboard - Visão Geral")
    
    # Carregar dados com cache - CORREÇÃO AQUI
    df = load_cached_data()
    
    if df.empty:
        st.warning("⚠️ Nenhum funcionário cadastrado. Vá para a seção 'Funcionários' para adicionar dados.", key="empty_warning")
        return
    
    # Criar cópia para manipulação - CORREÇÃO AQUI
    df_temp = df.copy()
    df_temp['data_admissao'] = pd.to_datetime(df_temp['data_admissao'])
    
    # Métricas principais
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_funcionarios = len(df_temp)
    salario_total = float(df_temp['salario'].sum())
    salario_medio = float(df_temp['salario'].mean())
    departamentos = int(df_temp['departamento'].nunique())
    
    # Funcionários recentes (últimos 30 dias)
    recent_hires = df_temp[df_temp['data_admissao'] >= (datetime.now() - pd.Timedelta(days=30))]
    
    with col1:
        st.metric("Total de Funcionários", total_funcionarios, key="total_metric_unique")
    
    with col2:
        st.metric("Folha Salarial Total", f"R$ {salario_total:,.2f}", key="salario_total_metric_unique")
    
    with col3:
        st.metric("Salário Médio", f"R$ {salario_medio:,.2f}", key="salario_medio_metric_unique")
    
    with col4:
        st.metric("Contratados Recentemente", len(recent_hires), delta=f"Últimos 30 dias", key="recent_metric_unique")
    
    with col5:
        st.metric("Departamentos", departamentos, key="dept_metric_unique")
    
    st.markdown("---")
    
    # Custo por Setor - Destaque Principal
    st.subheader("💰 Custo por Setor")
    
    # Calcular custo por departamento
    dept_costs = df_temp.groupby('departamento').agg({
        'salario': ['sum', 'mean', 'count']
    }).round(2)
    dept_costs.columns = ['Custo Total', 'Salário Médio', 'Funcionários']
    dept_costs = dept_costs.sort_values('Custo Total', ascending=False)
    
    # Gráfico principal de custo por setor
    fig_cost = px.bar(
        x=dept_costs.index,
        y=dept_costs['Custo Total'],
        title="💸 Custo Total por Setor",
        labels={'x': 'Departamento', 'y': 'Custo Total (R$)'},
        color=dept_costs['Custo Total'],
        color_continuous_scale=['#FF6B6B', '#FF0000', '#8B0000']
    )
    fig_cost.update_xaxes(tickangle=45)
    fig_cost.update_layout(height=400)
    st.plotly_chart(fig_cost, use_container_width=True, key="custo_setor_chart_unique")
    
    # Cartões de custo organizados em grid
    st.write("**💰 Resumo Detalhado por Setor:**")
    
    # Organizar em múltiplas colunas baseado no número de departamentos
    num_depts = len(dept_costs)
    if num_depts <= 3:
        cols = st.columns(num_depts)
    elif num_depts <= 6:
        cols = st.columns(3)
    else:
        cols = st.columns(4)
    
    for i, dept in enumerate(dept_costs.index):
        col_index = i % len(cols)
        
        with cols[col_index]:
            custo = dept_costs.loc[dept, 'Custo Total']
            funcionarios = int(dept_costs.loc[dept, 'Funcionários'])
            percentual = (custo / salario_total) * 100
            media_salarial = dept_costs.loc[dept, 'Salário Médio']
            
            # Cores baseadas no percentual de custo
            if percentual >= 20:
                border_color = "#FF0000"
                bg_color = "#330000"
            elif percentual >= 10:
                border_color = "#FF6B6B"
                bg_color = "#2A0000"
            else:
                border_color = "#FF9999"
                bg_color = "#220000"
            
            st.markdown(f"""
            <div style="
                border: 2px solid {border_color}; 
                padding: 12px; 
                margin: 5px 0; 
                border-radius: 8px;
                background: linear-gradient(135deg, {bg_color} 0%, #1E1E1E 100%);
                box-shadow: 0 2px 6px rgba(255, 0, 0, 0.3);
                height: 140px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                text-align: center;
            ">
                <div style="font-size: 14px; font-weight: bold; color: #FF0000; margin-bottom: 5px; 
                           white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {dept}
                </div>
                <div style="color: #FFFFFF; line-height: 1.3;">
                    <div style="font-size: 16px; font-weight: bold; margin-bottom: 3px;">
                        💰 R$ {custo/1000:.0f}K
                    </div>
                    <div style="font-size: 12px; color: #CCCCCC;">
                        📊 {percentual:.1f}%<br>
                        👥 {funcionarios} func.<br>
                        💵 R$ {media_salarial/1000:.1f}K
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Funcionários Recentes - Seção destacada
    if len(recent_hires) > 0:
        st.subheader("🆕 Funcionários Adicionados Recentemente")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Lista dos funcionários recentes
            recent_display = recent_hires[['nome', 'cargo', 'departamento', 'salario', 'data_admissao']].copy()
            recent_display['data_admissao'] = recent_display['data_admissao'].dt.strftime('%d/%m/%Y')
            recent_display = recent_display.sort_values('data_admissao', ascending=False)
            
            st.dataframe(
                recent_display,
                use_container_width=True,
                column_config={
                    "salario": st.column_config.NumberColumn(
                        "Salário",
                        format="R$ %.2f"
                    )
                },
                key="recent_employees_table_unique"
            )
        
        with col2:
            # Estatísticas dos funcionários recentes
            st.metric("Novos Funcionários", len(recent_hires), key="new_employees_metric_unique")
            st.metric("Custo Adicional", f"R$ {recent_hires['salario'].sum():,.2f}", key="new_cost_metric_unique")
            st.metric("Salário Médio (Novos)", f"R$ {recent_hires['salario'].mean():,.2f}", key="new_avg_salary_metric_unique")
    
    st.markdown("---")
    
    # Gráficos adicionais otimizados
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por departamento (máximo 8 departamentos)
        dept_count = df_temp['departamento'].value_counts()
        
        if len(dept_count) > 8:
            # Mostrar top 7 + "Outros"
            top_depts = dept_count.head(7)
            others_count = dept_count.tail(-7).sum()
            if others_count > 0:
                top_depts['Outros'] = others_count
            dept_count = top_depts
        
        fig_pie = px.pie(
            values=dept_count.values,
            names=dept_count.index,
            title="📊 Funcionários por Departamento",
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        st.plotly_chart(fig_pie, use_container_width=True, key="dept_pie_chart_unique")
    
    with col2:
        # Contratações ao longo do tempo
        if len(df_temp) > 0:
            monthly_hires = df_temp.groupby(df_temp['data_admissao'].dt.to_period('M')).size().reset_index()
            monthly_hires['data_admissao'] = monthly_hires['data_admissao'].astype(str)
            
            fig_line = px.line(
                monthly_hires,
                x='data_admissao',
                y=0,
                title="📈 Contratações por Mês",
                labels={'data_admissao': 'Mês', 0: 'Contratações'},
                color_discrete_sequence=['#FF0000']
            )
            st.plotly_chart(fig_line, use_container_width=True, key="hires_line_chart_unique")

# Função para gerenciar funcionários
def show_employees():
    st.header("👤 Gestão de Funcionários")
    
    # Tabs para diferentes operações
    tab1, tab2, tab3 = st.tabs(["📝 Adicionar", "👀 Visualizar", "✏️ Editar/Excluir"])
    
    with tab1:
        st.subheader("Adicionar Novo Funcionário")
        
        # Botão para adicionar múltiplos funcionários
        with st.expander("📋 Adicionar Múltiplos Funcionários (CSV)", key="multi_add_expander_unique"):
            st.write("**O sistema aceita automaticamente seus arquivos CSV do Excel**")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.success("✅ **Seu formato já é aceito!** O sistema detecta automaticamente:")
                st.markdown("""
                - **Separador**: Ponto e vírgula (;) ou vírgula (,)
                - **Salários**: Com ou sem R$, vírgulas para decimais
                - **Datas**: DD/MM/AAAA ou AAAA-MM-DD
                - **Colunas**: Com ou sem espaços nos nomes
                """)
                
                st.write("**Exemplo do seu formato:**")
                st.code("""nome;cargo; salario ;departamento;data admissao
JOÃO SILVA;ANALISTA; R$ 5.000,00 ;TECNOLOGIA;15/01/2024
MARIA SANTOS;GERENTE; R$ 8.500,50 ;VENDAS;01/02/2024""")
                
                st.info("💡 **Dica:** Salve direto do Excel como CSV e faça upload. O sistema converte automaticamente!")
            
            with col2:
                st.write("**Baixar Template:**")
                try:
                    with open('data/template_funcionarios.csv', 'r', encoding='utf-8') as template_file:
                        template_content = template_file.read()
                    st.download_button(
                        label="📥 Download Template CSV",
                        data=template_content,
                        file_name="template_funcionarios.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key="template_download_unique"
                    )
                except FileNotFoundError:
                    st.warning("Template não encontrado. Criando template padrão...")
                    template_content = "nome;cargo;salario;departamento;data_admissao\nExemplo;Analista;5000;Tecnologia;2024-01-01"
                    st.download_button(
                        label="📥 Download Template CSV",
                        data=template_content,
                        file_name="template_funcionarios.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key="template_download_fallback_unique"
                    )
                
                st.write("**Como usar:**")
                st.markdown("""
                1. Baixe o template (formato Excel padrão)
                2. Edite no Excel normalmente
                3. Salve como CSV
                4. Faça upload - conversão automática!
                
                **Formatos aceitos:**
                - Salário: R$ 1.500,00 ou 1500
                - Data: 15/01/2024 ou 2024-01-15
                - Separador: ; ou ,
                """)
            
            uploaded_file = st.file_uploader("Selecionar arquivo CSV", type=['csv'], key="csv_uploader_unique")
            if uploaded_file is not None:
                # Prévia dos dados
                try:
                    # Reset file pointer
                    uploaded_file.seek(0)
                    
                    # Tentar diferentes separadores e encodings
                    preview_df = None
                    error_messages = []
                    
                    # Lista de configurações para tentar
                    configs = [
                        {'sep': ';', 'encoding': 'utf-8'},
                        {'sep': ';', 'encoding': 'latin-1'},
                        {'sep': ';', 'encoding': 'cp1252'},
                        {'sep': ';', 'encoding': 'iso-8859-1'},
                        {'sep': ',', 'encoding': 'utf-8'},
                        {'sep': ',', 'encoding': 'latin-1'},
                    ]
                    
                    for config in configs:
                        try:
                            uploaded_file.seek(0)
                            preview_df = pd.read_csv(uploaded_file, sep=config['sep'], encoding=config['encoding'])
                            if len(preview_df.columns) > 0 and len(preview_df) > 0:
                                break
                            else:
                                error_messages.append(f"Config {config}: arquivo vazio ou sem colunas")
                        except Exception as e:
                            error_messages.append(f"Config {config}: {str(e)}")
                            continue
                    
                    if preview_df is None or len(preview_df.columns) == 0:
                        st.error("❌ Erro ao ler arquivo CSV: Não foi possível detectar o formato")
                        st.write("**Tentativas realizadas:**")
                        for msg in error_messages:
                            st.write(f"- {msg}")
                        st.info("💡 Certifique-se de que o arquivo tem dados e está no formato CSV correto")
                        return
                    
                    # Limpar nomes das colunas (remover espaços)
                    preview_df.columns = preview_df.columns.str.strip()
                    
                    # Mapear colunas com nomes alternativos
                    column_mapping = {
                        'data admissao': 'data_admissao',
                        'data_admissao': 'data_admissao',
                        'salario': 'salario',
                        ' salario ': 'salario'
                    }
                    
                    for old_name, new_name in column_mapping.items():
                        if old_name in preview_df.columns:
                            preview_df = preview_df.rename(columns={old_name: new_name})
                    
                    # Verificar se todas as colunas obrigatórias estão presentes
                    required_columns = ['nome', 'cargo', 'salario', 'departamento', 'data_admissao']
                    missing_columns = [col for col in required_columns if col not in preview_df.columns]
                    
                    if missing_columns:
                        st.error(f"❌ Colunas obrigatórias faltando: {', '.join(missing_columns)}")
                        st.write("**Colunas encontradas no arquivo:**", list(preview_df.columns))
                        st.write("**Colunas obrigatórias:**", required_columns)
                    else:
                        st.success("✅ Todas as colunas obrigatórias encontradas!")
                        
                        st.write("**Prévia dos dados:**")
                        st.dataframe(preview_df.head(), use_container_width=True, key="preview_table_unique")
                        
                        st.write(f"**Total de funcionários no arquivo:** {len(preview_df)}")
                        
                        if st.button("📂 Importar Funcionários", key="import_button_unique"):
                            success_count = 0
                            error_count = 0
                            errors_list = []
                            
                            for index, row in preview_df.iterrows():
                                try:
                                    # Criar email automático baseado no nome
                                    nome_parts = str(row['nome']).lower().split()
                                    if len(nome_parts) >= 2:
                                        email = f"{nome_parts[0]}.{nome_parts[-1]}@empresa.com"
                                    else:
                                        email = f"{nome_parts[0]}@empresa.com"
                                    
                                    # Limpar valor do salário (remover R$, espaços e converter vírgula para ponto)
                                    salario_str = str(row['salario']).strip()
                                    salario_str = salario_str.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
                                    try:
                                        salario_value = float(salario_str)
                                    except:
                                        salario_value = 0.0
                                    
                                    # Converter data do formato DD/MM/AAAA para AAAA-MM-DD
                                    data_str = str(row['data_admissao']).strip()
                                    if '/' in data_str:
                                        parts = data_str.split('/')
                                        if len(parts) == 3:
                                            data_formatted = f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
                                        else:
                                            data_formatted = data_str
                                    else:
                                        data_formatted = data_str
                                    
                                    employee_data = {
                                        'nome': str(row['nome']).strip(),
                                        'email': email,
                                        'telefone': '',
                                        'departamento': str(row['departamento']).strip(),
                                        'cargo': str(row['cargo']).strip(),
                                        'salario': salario_value,
                                        'data_admissao': data_formatted,
                                        'status': 'Ativo',
                                        'observacoes': ''
                                    }
                                    
                                    if data_handler.add_employee(employee_data):
                                        success_count += 1
                                    else:
                                        error_count += 1
                                        errors_list.append(f"Linha {index + 2}: {row['nome']} (email já existe)")
                                except Exception as e:
                                    error_count += 1
                                    errors_list.append(f"Linha {index + 2}: {row['nome']} - {str(e)}")
                            
                            if success_count > 0:
                                st.success(f"✅ {success_count} funcionários importados com sucesso!")
                            if error_count > 0:
                                st.warning(f"⚠️ {error_count} funcionários não foram importados")
                                with st.expander("Ver detalhes dos erros"):
                                    for error in errors_list:
                                        st.write(f"- {error}")
                            st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao ler arquivo CSV: {str(e)}")
                    st.write("**Possíveis problemas:**")
                    st.write("- Arquivo não está em formato CSV")
                    st.write("- Encoding do arquivo (tente salvar como UTF-8)")
                    st.write("- Separador incorreto (deve ser vírgula)")
                    st.write("- Verifique se as colunas estão nomeadas corretamente")
        
        st.markdown("---")
        
        with st.form("add_employee_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome Completo*", key="nome_input_unique")
                cargo = st.text_input("Cargo*", key="cargo_input_unique")
                salario = st.number_input("Salário (R$)*", min_value=0.0, step=100.0, key="salario_input_unique")
            
            with col2:
                departamento = st.selectbox("Departamento*", 
                    ["Recursos Humanos", "Tecnologia", "Vendas", "Marketing", "Financeiro", "Operações", "Outro"],
                    key="dept_select_unique")
                data_admissao = st.date_input("Data de Admissão*", value=date.today(), key="date_input_unique")
                
                # Campos opcionais em expander
                with st.expander("📋 Campos Opcionais", key="optional_expander_unique"):
                    email_opt = st.text_input("Email (será gerado automaticamente se vazio)", key="email_input_unique")
                    telefone_opt = st.text_input("Telefone", key="phone_input_unique")
                    status_opt = st.selectbox("Status", ["Ativo", "Inativo", "Férias"], key="status_select_unique")
                    observacoes_opt = st.text_area("Observações", key="obs_input_unique")
            
            submitted = st.form_submit_button("➕ Adicionar Funcionário", key="add_employee_btn_unique")
            
            if submitted:
                if nome and departamento and cargo and salario > 0:
                    # Gerar email automaticamente se não fornecido
                    if not email_opt:
                        nome_parts = nome.lower().split()
                        if len(nome_parts) >= 2:
                            email_final = f"{nome_parts[0]}.{nome_parts[-1]}@empresa.com"
                        else:
                            email_final = f"{nome_parts[0]}@empresa.com"
                    else:
                        email_final = email_opt
                    
                    success = data_handler.add_employee({
                        'nome': nome,
                        'email': email_final,
                        'telefone': telefone_opt,
                        'departamento': departamento,
                        'cargo': cargo,
                        'salario': salario,
                        'data_admissao': data_admissao,
                        'status': status_opt,
                        'observacoes': observacoes_opt
                    })
                    
                    if success:
                        st.success("✅ Funcionário adicionado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar funcionário. Email já existe.")
                else:
                    st.error("⚠️ Por favor, preencha os campos obrigatórios: Nome, Departamento, Cargo e Salário.")
    
    with tab2:
        st.subheader("Lista de Funcionários")
        
        # Carregar dados
        df = load_cached_data()
        
        if df.empty:
            st.info("📭 Nenhum funcionário cadastrado.", key="empty_info")
            return
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dept_filter = st.selectbox("Filtrar por Departamento", ["Todos"] + list(df['departamento'].unique()), key="dept_filter_unique")
        
        with col2:
            status_filter = st.selectbox("Filtrar por Status", ["Todos"] + list(df['status'].unique()), key="status_filter_unique")
        
        with col3:
            search_term = st.text_input("🔍 Buscar por nome", key="search_input_unique")
        
        # Aplicar filtros
        filtered_df = df.copy()
        
        if dept_filter != "Todos":
            filtered_df = filtered_df[filtered_df['departamento'] == dept_filter]
        
        if status_filter != "Todos":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        if search_term:
            filtered_df = filtered_df[filtered_df['nome'].str.contains(search_term, case=False, na=False)]
        
        # Opções de visualização
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            view_mode = st.radio("Modo de visualização:", ["📋 Tabela", "📊 Cartões"], horizontal=True, key="view_mode_radio_unique")
        with col2:
            sort_by = st.selectbox("Ordenar por:", ["nome", "salario", "data_admissao", "departamento"], key="sort_select_unique")
        with col3:
            sort_order = st.selectbox("Ordem:", ["Crescente", "Decrescente"], key="order_select_unique")
        
        # Aplicar ordenação
        ascending = True if sort_order == "Crescente" else False
        if not filtered_df.empty:
            filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
        
        if view_mode == "📋 Tabela":
            # Exibir tabela com edição rápida
            st.dataframe(
                filtered_df[['nome', 'email', 'departamento', 'cargo', 'salario', 'status', 'data_admissao']],
                use_container_width=True,
                key="employees_table_unique"
            )
            
            # Edição rápida de status
            with st.expander("⚡ Edição Rápida de Status", key="quick_edit_expander_unique"):
                selected_employees = st.multiselect("Selecionar funcionários:", filtered_df['nome'].tolist(), key="employee_select_unique")
                new_status = st.selectbox("Novo status:", ["Ativo", "Inativo", "Férias"], key="new_status_select_unique")
                
                if st.button("💾 Atualizar Status Selecionados", key="update_status_btn_unique") and selected_employees:
                    updated_count = 0
                    for emp_name in selected_employees:
                        emp_data_row = filtered_df[filtered_df['nome'] == emp_name].iloc[0]
                        emp_email = emp_data_row['email']
                        emp_data = filtered_df[filtered_df['nome'] == emp_name].iloc[0].to_dict()
                        emp_data['status'] = new_status
                        
                        if data_handler.update_employee(emp_email, emp_data):
                            updated_count += 1
                    
                    if updated_count > 0:
                        st.success(f"✅ {updated_count} funcionários atualizados!")
                        st.rerun()
        else:
            # Visualização em cartões
            for idx, row in filtered_df.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**{row['nome']}**")
                        st.write(f"📧 {row['email']}")
                        st.write(f"📱 {row.get('telefone', 'N/A')}")
                    
                    with col2:
                        st.write(f"🏢 {row['departamento']}")
                        st.write(f"💼 {row['cargo']}")
                        st.write(f"💰 R$ {row['salario']:,.2f}")
                    
                    with col3:
                        status_color = "🟢" if row['status'] == "Ativo" else ("🟡" if row['status'] == "Férias" else "🔴")
                        st.write(f"{status_color} {row['status']}")
                        st.write(f"📅 {row['data_admissao']}")
                    
                    st.markdown("---")
        
        st.info(f"📊 Mostrando {len(filtered_df)} de {len(df)} funcionários", key="filter_info")
    
    with tab3:
        st.subheader("Editar ou Excluir Funcionário")
        
        df = load_cached_data()
        
        if df.empty:
            st.info("📭 Nenhum funcionário cadastrado.", key="empty_info_edit")
            return
        
        # Selecionar funcionário
        employee_names = df['nome'].tolist()
        selected_employee = st.selectbox("Selecione um funcionário:", employee_names, key="employee_edit_select_unique")
        
        if selected_employee:
            employee_data = df[df['nome'] == selected_employee].iloc[0]
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader("Editar Funcionário")
                
                with st.form("edit_employee_form", key="edit_form_unique"):
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        nome = st.text_input("Nome Completo", value=employee_data['nome'], key="edit_nome_unique")
                        email = st.text_input("Email", value=employee_data['email'], key="edit_email_unique")
                        telefone = st.text_input("Telefone", value=employee_data.get('telefone', ''), key="edit_telefone_unique")
                        departamento = st.selectbox("Departamento", 
                            ["Recursos Humanos", "Tecnologia", "Vendas", "Marketing", "Financeiro", "Operações", "Outro"],
                            index=["Recursos Humanos", "Tecnologia", "Vendas", "Marketing", "Financeiro", "Operações", "Outro"].index(employee_data['departamento']) if employee_data['departamento'] in ["Recursos Humanos", "Tecnologia", "Vendas", "Marketing", "Financeiro", "Operações", "Outro"] else 0,
                            key="edit_departamento_unique")
                    
                    with col_b:
                        cargo = st.text_input("Cargo", value=employee_data['cargo'], key="edit_cargo_unique")
                        salario = st.number_input("Salário (R$)", value=float(employee_data['salario']), min_value=0.0, step=100.0, key="edit_salario_unique")
                        data_admissao = st.date_input("Data de Admissão", value=pd.to_datetime(employee_data['data_admissao']).date(), key="edit_data_admissao_unique")
                        status = st.selectbox("Status", ["Ativo", "Inativo", "Férias"],
                            index=["Ativo", "Inativo", "Férias"].index(employee_data['status']) if employee_data['status'] in ["Ativo", "Inativo", "Férias"] else 0,
                            key="edit_status_unique")
                    
                    observacoes = st.text_area("Observações", value=employee_data.get('observacoes', ''), key="edit_observacoes_unique")
                    
                    submitted = st.form_submit_button("💾 Salvar Alterações", key="save_edit_btn_unique")
                    
                    if submitted:
                        updated_data = {
                            'nome': nome,
                            'email': email,
                            'telefone': telefone,
                            'departamento': departamento,
                            'cargo': cargo,
                            'salario': salario,
                            'data_admissao': data_admissao,
                            'status': status,
                            'observacoes': observacoes
                        }
                        
                        if data_handler.update_employee(employee_data['email'], updated_data):
                            st.success("✅ Funcionário atualizado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao atualizar funcionário.")
            
            with col2:
                st.subheader("Excluir")
                st.warning("⚠️ Esta ação não pode ser desfeita!", key="delete_warning")
                
                if st.button("🗑️ Excluir Funcionário", type="secondary", key="delete_btn_unique"):
                    if data_handler.delete_employee(employee_data['email']):
                        st.success("✅ Funcionário excluído com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao excluir funcionário.")

# Função para relatórios
def show_reports():
    st.header("📊 Relatórios e Análises")
    
    df = load_cached_data()
    
    if df.empty:
        st.warning("⚠️ Nenhum dado disponível para gerar relatórios.", key="reports_warning")
        return
    
    # Criar cópia para manipulação - CORREÇÃO AQUI
    df_temp = df.copy()
    df_temp['data_admissao'] = pd.to_datetime(df_temp['data_admissao'])
    
    # Filtros de período
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Data Inicial", value=df_temp['data_admissao'].min().date(), key="start_date_unique")
    with col2:
        end_date = st.date_input("Data Final", value=date.today(), key="end_date_unique")
    
    # Filtrar dados por período
    df_filtered = df_temp[
        (df_temp['data_admissao'].dt.date >= start_date) &
        (df_temp['data_admissao'].dt.date <= end_date)
    ]
    
    # Tabs para diferentes tipos de relatórios
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Salários", "📈 Crescimento", "🏢 Departamentos", "📋 Exportar"])
    
    with tab1:
        st.subheader("Análise Salarial")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histograma de salários
            fig_hist = px.histogram(
                df_filtered,
                x='salario',
                nbins=20,
                title="Distribuição de Salários"
            )
            st.plotly_chart(fig_hist, use_container_width=True, key="salary_hist_chart_unique")
        
        with col2:
            # Top 10 maiores salários
            top_salaries = df_filtered.nlargest(10, 'salario')
            fig_top = px.bar(
                top_salaries,
                x='nome',
                y='salario',
                title="Top 10 Maiores Salários"
            )
            fig_top.update_xaxes(tickangle=45)
            st.plotly_chart(fig_top, use_container_width=True, key="top_salaries_chart_unique")
        
        # Estatísticas salariais por departamento
        salary_stats = df_filtered.groupby('departamento')['salario'].agg(['mean', 'median', 'min', 'max']).round(2)
        salary_stats.columns = ['Média', 'Mediana', 'Mínimo', 'Máximo']
        st.subheader("Estatísticas Salariais por Departamento")
        st.dataframe(salary_stats, use_container_width=True, key="salary_stats_table_unique")
    
    with tab2:
        st.subheader("Crescimento da Empresa")
        
        # Contratações ao longo do tiempo
        monthly_hires = df_filtered.groupby(df_filtered['data_admissao'].dt.to_period('M')).size().reset_index()
        monthly_hires['data_admissao'] = monthly_hires['data_admissao'].astype(str)
        
        fig_growth = px.line(
            monthly_hires,
            x='data_admissao',
            y=0,
            title="Contratações por Mês"
        )
        fig_growth.update_layout(yaxis_title="Número de Contratações")
        st.plotly_chart(fig_growth, use_container_width=True, key="growth_chart_unique")
        
        # Crescimento cumulativo
        cumulative_hires = df_filtered.sort_values('data_admissao')
        cumulative_hires['funcionarios_acumulados'] = range(1, len(cumulative_hires) + 1)
        
        fig_cumulative = px.line(
            cumulative_hires,
            x='data_admissao',
            y='funcionarios_acumulados',
            title="Crescimento Cumulativo de Funcionários"
        )
        st.plotly_chart(fig_cumulative, use_container_width=True, key="cumulative_chart_unique")
    
    with tab3:
        st.subheader("🏢 Análise Completa por Departamentos")
        
        # Análise detalhada com múltiplas métricas
        dept_analysis = df_filtered.groupby('departamento').agg({
            'salario': ['sum', 'mean', 'median', 'count', 'min', 'max'],
            'nome': 'count'
        }).round(2)
        dept_analysis.columns = ['Custo Total', 'Média Salarial', 'Mediana', 'Funcionários', 'Menor Salário', 'Maior Salário', 'Total']
        dept_analysis = dept_analysis.drop('Total', axis=1)  # Remove coluna duplicada
        dept_analysis = dept_analysis.sort_values('Custo Total', ascending=False)
        
        # Calcular percentuais
        total_custo = dept_analysis['Custo Total'].sum()
        dept_analysis['% do Custo Total'] = (dept_analysis['Custo Total'] / total_custo * 100).round(1)
        
        # Mostrar tabela com formatação de moeda
        st.subheader("📊 Resumo Financeiro por Departamento")
        st.dataframe(
            dept_analysis,
            use_container_width=True,
            column_config={
                "Custo Total": st.column_config.NumberColumn("Custo Total", format="R$ %.2f"),
                "Média Salarial": st.column_config.NumberColumn("Média Salarial", format="R$ %.2f"),
                "Mediana": st.column_config.NumberColumn("Mediana", format="R$ %.2f"),
                "Menor Salário": st.column_config.NumberColumn("Menor Salário", format="R$ %.2f"),
                "Maior Salário": st.column_config.NumberColumn("Maior Salário", format="R$ %.2f"),
                "% do Custo Total": st.column_config.NumberColumn("% do Custo Total", format="%.1f%%")
            },
            key="dept_analysis_table_unique"
        )
        
        # Gráficos aprimorados
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de custo vs funcionários (otimizado para muitos departamentos)
            dept_display = dept_analysis.head(10)  # Top 10 departamentos
            
            if len(dept_analysis) > 10:
                others_cost = dept_analysis.tail(-10)['Custo Total'].sum()
                others_func = dept_analysis.tail(-10)['Funcionários'].sum()
                
                # Adicionar "Outros" se necessário
                new_row = pd.DataFrame({
                    'Custo Total': [others_cost],
                    'Funcionários': [others_func],
                    'Média Salarial': [others_cost/others_func if others_func > 0 else 0]
                }, index=['Outros'])
                dept_display = pd.concat([dept_display, new_row])
            
            # Reset index para criar coluna 'departamento'
            dept_scatter = dept_display.reset_index()
            dept_scatter = dept_scatter.rename(columns={'index': 'departamento'})
            
            fig_scatter = px.scatter(
                dept_scatter,
                x='Funcionários',
                y='Custo Total',
                title="💰 Custo Total vs Número de Funcionários",
                text='departamento',
                size='Custo Total',
                color='Média Salarial',
                color_continuous_scale='Reds',
                hover_data=['Média Salarial']
            )
            fig_scatter.update_traces(textposition="top center")
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True, key="scatter_chart_unique")
        
        with col2:
            # Participação no custo total (pizza)
            dept_pie = dept_display.reset_index()
            dept_pie = dept_pie.rename(columns={'index': 'departamento'})
            
            fig_pie_cost = px.pie(
                dept_pie,
                values='Custo Total',
                names='departamento',
                title="📊 Participação no Custo Total",
                color_discrete_sequence=px.colors.sequential.Reds_r
            )
            fig_pie_cost.update_layout(height=400)
            st.plotly_chart(fig_pie_cost, use_container_width=True, key="pie_chart_unique")
        
        # Análise de eficiência salarial
        st.subheader("⚡ Análise de Eficiência")
        
        # Calcular eficiência (custo médio por funcionário)
        dept_analysis['Custo por Funcionário'] = dept_analysis['Custo Total'] / dept_analysis['Funcionários']
        dept_efficiency = dept_analysis.sort_values('Custo por Funcionário', ascending=False).head(10)
        
        # Preparar dados para o gráfico de eficiência
        dept_eff = dept_efficiency.reset_index()
        dept_eff = dept_eff.rename(columns={'index': 'departamento'})
        
        fig_efficiency = px.bar(
            dept_eff,
            x='departamento',
            y='Custo por Funcionário',
            title="💸 Custo Médio por Funcionário (Top 10)",
            color='Custo por Funcionário',
            color_continuous_scale='Reds',
            text='Custo por Funcionário'
        )
        fig_efficiency.update_xaxes(tickangle=45)
        fig_efficiency.update_traces(texttemplate='R$ %{text:,.0f}', textposition='outside')
        st.plotly_chart(fig_efficiency, use_container_width=True, key="efficiency_chart_unique")
    
    with tab4:
        st.subheader("Exportar Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Exportar Lista Completa de Funcionários**")
            if st.button("📊 Baixar Excel - Funcionários", key="export_employees_btn_unique"):
                excel_data = data_handler.export_to_excel(df_filtered)
                if excel_data:
                    st.download_button(
                        label="⬇️ Download Excel",
                        data=excel_data,
                        file_name=f"funcionarios_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_excel_btn_unique"
                    )
        
        with col2:
            st.write("**Exportar Relatório de Salários**")
            if st.button("📈 Baixar Relatório de Salários", key="export_salary_btn_unique"):
                salary_report = df_filtered.groupby('departamento').agg({
                    'nome': 'count',
                    'salario': ['mean', 'sum', 'min', 'max']
                }).round(2)
                
                excel_data = data_handler.export_salary_report(salary_report)
                if excel_data:
                    st.download_button(
                        label="⬇️ Download Relatório",
                        data=excel_data,
                        file_name=f"relatorio_salarios_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_report_btn_unique"
                    )

# Função para configurações
def show_settings():
    st.header("⚙️ Configurações do Sistema")
    
    st.subheader("🔧 Manutenção de Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Backup dos Dados**")
        if st.button("💾 Criar Backup", key="backup_btn_unique"):
            backup_data = data_handler.create_backup()
            if backup_data:
                st.download_button(
                    label="⬇️ Download Backup",
                    data=backup_data,
                    file_name=f"backup_funcionarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    key="download_backup_btn_unique"
                )
                st.success("✅ Backup criado com sucesso!")
            else:
                st.error("❌ Erro ao criar backup.")
    
    with col2:
        st.write("**Restaurar Dados**")
        uploaded_file = st.file_uploader("Carregar arquivo de backup", type=['csv'], key="restore_uploader_unique")
        if uploaded_file is not None:
            if st.button("🔄 Restaurar Dados", key="restore_btn_unique"):
                if data_handler.restore_backup(uploaded_file):
                    st.success("✅ Dados restaurados com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao restaurar dados. Verifique o formato do arquivo.")
    
    st.markdown("---")
    
    st.subheader("📊 Informações do Sistema")
    
    df = load_cached_data()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Registros", len(df), key="total_records_metric_unique")
    
    with col2:
        if not df.empty:
            last_update = pd.to_datetime(df['data_admissao']).max()
            st.metric("Última Atualização", last_update.strftime('%d/%m/%Y'), key="last_update_metric_unique")
        else:
            st.metric("Última Atualização", "Nunca", key="never_update_metric_unique")
    
    with col3:
        file_size = os.path.getsize(data_handler.data_file) if os.path.exists(data_handler.data_file) else 0
        st.metric("Tamanho do Arquivo", f"{file_size / 1024:.1f} KB", key="file_size_metric_unique")

# Roteamento principal
if page == "🏠 Dashboard":
    show_dashboard()
elif page == "👤 Funcionários":
    show_employees()
elif page == "📊 Relatórios":
    show_reports()
elif page == "⚙️ Configurações":
    show_settings()

# Footer
st.markdown("---")
st.markdown("© 2025 Sistema de Gestão de Funcionários - Desenvolvido com Streamlit")
