import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import os
from utils.data_handler import DataHandler
from utils.visualizations import create_visualizations

# Configuração da página
st.set_page_config(
    page_title="Sistema de Gestão de Funcionários",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar o manipulador de dados
@st.cache_resource
def get_data_handler():
    return DataHandler()

data_handler = get_data_handler()

# Título principal
st.title("👥 Sistema de Gestão de Funcionários")
st.markdown("---")

# Sidebar para navegação
st.sidebar.title("📋 Menu de Navegação")

# Botão de atualização automática
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Atualizar Dados", use_container_width=True):
    st.cache_resource.clear()
    st.rerun()

# Informações em tempo real
df = data_handler.load_data()
if not df.empty:
    st.sidebar.metric("Total de Funcionários", len(df))
    st.sidebar.metric("Folha Salarial", f"R$ {df['salario'].sum():,.2f}")
    st.sidebar.metric("Último Update", datetime.now().strftime("%H:%M:%S"))

st.sidebar.markdown("---")
page = st.sidebar.selectbox(
    "Selecione uma opção:",
    ["🏠 Dashboard", "👤 Funcionários", "📊 Relatórios", "⚙️ Configurações"]
)

# Função para exibir dashboard
def show_dashboard():
    st.header("📊 Dashboard - Visão Geral")
    
    # Carregar dados
    df = data_handler.load_data()
    
    if df.empty:
        st.warning("⚠️ Nenhum funcionário cadastrado. Vá para a seção 'Funcionários' para adicionar dados.")
        return
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    total_funcionarios = len(df)
    salario_total = float(df['salario'].sum())
    salario_medio = float(df['salario'].mean())
    departamentos = int(df['departamento'].nunique())
    
    with col1:
        st.metric("Total de Funcionários", total_funcionarios)
    
    with col2:
        st.metric("Folha Salarial Total", f"R$ {salario_total:,.2f}")
    
    with col3:
        st.metric("Salário Médio", f"R$ {salario_medio:,.2f}")
    
    with col4:
        st.metric("Departamentos", departamentos)
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Funcionários por departamento
        dept_count = df['departamento'].value_counts()
        fig_dept = px.pie(
            values=dept_count.values,
            names=dept_count.index,
            title="Funcionários por Departamento"
        )
        fig_dept.update_layout(height=400)
        st.plotly_chart(fig_dept, use_container_width=True)
    
    with col2:
        # Distribuição salarial por departamento
        fig_salary = px.box(
            df,
            x='departamento',
            y='salario',
            title="Distribuição Salarial por Departamento"
        )
        fig_salary.update_layout(height=400)
        fig_salary.update_xaxes(tickangle=45)
        st.plotly_chart(fig_salary, use_container_width=True)
    
    # Tabela de funcionários recentes
    st.subheader("📅 Funcionários Adicionados Recentemente")
    recent_employees = df.sort_values('data_admissao', ascending=False).head(5)
    st.dataframe(recent_employees[['nome', 'departamento', 'cargo', 'salario', 'data_admissao']], use_container_width=True)

# Função para gerenciar funcionários
def show_employees():
    st.header("👤 Gestão de Funcionários")
    
    # Tabs para diferentes operações
    tab1, tab2, tab3 = st.tabs(["📝 Adicionar", "👀 Visualizar", "✏️ Editar/Excluir"])
    
    with tab1:
        st.subheader("Adicionar Novo Funcionário")
        
        # Botão para adicionar múltiplos funcionários
        with st.expander("📋 Adicionar Múltiplos Funcionários (CSV)"):
            st.write("Faça upload de um arquivo CSV com as colunas: nome, email, telefone, departamento, cargo, salario, data_admissao, status, observacoes")
            uploaded_file = st.file_uploader("Selecionar arquivo CSV", type=['csv'])
            if uploaded_file is not None:
                if st.button("📂 Importar Funcionários"):
                    try:
                        import_df = pd.read_csv(uploaded_file)
                        success_count = 0
                        error_count = 0
                        
                        for _, row in import_df.iterrows():
                            employee_data = row.to_dict()
                            if data_handler.add_employee(employee_data):
                                success_count += 1
                            else:
                                error_count += 1
                        
                        if success_count > 0:
                            st.success(f"✅ {success_count} funcionários importados com sucesso!")
                        if error_count > 0:
                            st.warning(f"⚠️ {error_count} funcionários não foram importados (email já existe)")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao importar arquivo: {e}")
        
        st.markdown("---")
        
        with st.form("add_employee_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome Completo*")
                email = st.text_input("Email*")
                telefone = st.text_input("Telefone")
                departamento = st.selectbox("Departamento*", 
                    ["Recursos Humanos", "Tecnologia", "Vendas", "Marketing", "Financeiro", "Operações", "Outro"])
            
            with col2:
                cargo = st.text_input("Cargo*")
                salario = st.number_input("Salário (R$)*", min_value=0.0, step=100.0)
                data_admissao = st.date_input("Data de Admissão*", value=date.today())
                status = st.selectbox("Status", ["Ativo", "Inativo", "Férias"])
            
            observacoes = st.text_area("Observações")
            
            submitted = st.form_submit_button("➕ Adicionar Funcionário")
            
            if submitted:
                if nome and email and departamento and cargo and salario > 0:
                    success = data_handler.add_employee({
                        'nome': nome,
                        'email': email,
                        'telefone': telefone,
                        'departamento': departamento,
                        'cargo': cargo,
                        'salario': salario,
                        'data_admissao': data_admissao,
                        'status': status,
                        'observacoes': observacoes
                    })
                    
                    if success:
                        st.success("✅ Funcionário adicionado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar funcionário. Email já existe.")
                else:
                    st.error("⚠️ Por favor, preencha todos os campos obrigatórios.")
    
    with tab2:
        st.subheader("Lista de Funcionários")
        
        # Carregar dados
        df = data_handler.load_data()
        
        if df.empty:
            st.info("📭 Nenhum funcionário cadastrado.")
            return
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dept_filter = st.selectbox("Filtrar por Departamento", ["Todos"] + list(df['departamento'].unique()))
        
        with col2:
            status_filter = st.selectbox("Filtrar por Status", ["Todos"] + list(df['status'].unique()))
        
        with col3:
            search_term = st.text_input("🔍 Buscar por nome")
        
        # Aplicar filtros
        filtered_df = df.copy()
        
        if dept_filter != "Todos":
            filtered_df = filtered_df[filtered_df['departamento'] == dept_filter]
        
        if status_filter != "Todos":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        if search_term:
            filtered_df = filtered_df[filtered_df['nome'].astype(str).str.contains(search_term, case=False, na=False)]
        
        # Opções de visualização
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            view_mode = st.radio("Modo de visualização:", ["📋 Tabela", "📊 Cartões"], horizontal=True)
        with col2:
            sort_by = st.selectbox("Ordenar por:", ["nome", "salario", "data_admissao", "departamento"])
        with col3:
            sort_order = st.selectbox("Ordem:", ["Crescente", "Decrescente"])
        
        # Aplicar ordenação
        ascending = True if sort_order == "Crescente" else False
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
        
        if view_mode == "📋 Tabela":
            # Exibir tabela com edição rápida
            st.dataframe(
                filtered_df[['nome', 'email', 'departamento', 'cargo', 'salario', 'status', 'data_admissao']],
                use_container_width=True
            )
            
            # Edição rápida de status
            with st.expander("⚡ Edição Rápida de Status"):
                selected_employees = st.multiselect("Selecionar funcionários:", filtered_df['nome'].tolist())
                new_status = st.selectbox("Novo status:", ["Ativo", "Inativo", "Férias"])
                
                if st.button("💾 Atualizar Status Selecionados") and selected_employees:
                    updated_count = 0
                    for emp_name in selected_employees:
                        emp_email = filtered_df[filtered_df['nome'] == emp_name]['email'].iloc[0]
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
        
        st.info(f"📊 Mostrando {len(filtered_df)} de {len(df)} funcionários")
    
    with tab3:
        st.subheader("Editar ou Excluir Funcionário")
        
        df = data_handler.load_data()
        
        if df.empty:
            st.info("📭 Nenhum funcionário cadastrado.")
            return
        
        # Selecionar funcionário
        employee_names = df['nome'].tolist()
        selected_employee = st.selectbox("Selecione um funcionário:", employee_names)
        
        if selected_employee:
            employee_data = df[df['nome'] == selected_employee].iloc[0]
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader("Editar Funcionário")
                
                with st.form("edit_employee_form"):
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        nome = st.text_input("Nome Completo", value=employee_data['nome'])
                        email = st.text_input("Email", value=employee_data['email'])
                        telefone = st.text_input("Telefone", value=employee_data.get('telefone', ''))
                        departamento = st.selectbox("Departamento", 
                            ["Recursos Humanos", "Tecnologia", "Vendas", "Marketing", "Financeiro", "Operações", "Outro"],
                            index=["Recursos Humanos", "Tecnologia", "Vendas", "Marketing", "Financeiro", "Operações", "Outro"].index(employee_data['departamento']) if employee_data['departamento'] in ["Recursos Humanos", "Tecnologia", "Vendas", "Marketing", "Financeiro", "Operações", "Outro"] else 0)
                    
                    with col_b:
                        cargo = st.text_input("Cargo", value=employee_data['cargo'])
                        salario = st.number_input("Salário (R$)", value=float(employee_data['salario']), min_value=0.0, step=100.0)
                        data_admissao = st.date_input("Data de Admissão", value=pd.to_datetime(employee_data['data_admissao']).date())
                        status = st.selectbox("Status", ["Ativo", "Inativo", "Férias"],
                            index=["Ativo", "Inativo", "Férias"].index(employee_data['status']) if employee_data['status'] in ["Ativo", "Inativo", "Férias"] else 0)
                    
                    observacoes = st.text_area("Observações", value=employee_data.get('observacoes', ''))
                    
                    submitted = st.form_submit_button("💾 Salvar Alterações")
                    
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
                st.warning("⚠️ Esta ação não pode ser desfeita!")
                
                if st.button("🗑️ Excluir Funcionário", type="secondary"):
                    if data_handler.delete_employee(employee_data['email']):
                        st.success("✅ Funcionário excluído com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao excluir funcionário.")

# Função para relatórios
def show_reports():
    st.header("📊 Relatórios e Análises")
    
    df = data_handler.load_data()
    
    if df.empty:
        st.warning("⚠️ Nenhum dado disponível para gerar relatórios.")
        return
    
    # Filtros de período
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Data Inicial", value=pd.to_datetime(df['data_admissao']).min().date())
    with col2:
        end_date = st.date_input("Data Final", value=date.today())
    
    # Filtrar dados por período
    df_filtered = df[
        (pd.to_datetime(df['data_admissao']).dt.date >= start_date) &
        (pd.to_datetime(df['data_admissao']).dt.date <= end_date)
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
            st.plotly_chart(fig_hist, use_container_width=True)
        
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
            st.plotly_chart(fig_top, use_container_width=True)
        
        # Estatísticas salariais por departamento
        salary_stats = df_filtered.groupby('departamento')['salario'].agg(['mean', 'median', 'min', 'max']).round(2)
        salary_stats.columns = ['Média', 'Mediana', 'Mínimo', 'Máximo']
        st.subheader("Estatísticas Salariais por Departamento")
        st.dataframe(salary_stats, use_container_width=True)
    
    with tab2:
        st.subheader("Crescimento da Empresa")
        
        # Contratações ao longo do tempo
        df_filtered_copy = df_filtered.copy()
        df_filtered_copy['data_admissao'] = pd.to_datetime(df_filtered_copy['data_admissao'])
        monthly_hires = df_filtered_copy.groupby(df_filtered_copy['data_admissao'].dt.to_period('M')).size().reset_index()
        monthly_hires['data_admissao'] = monthly_hires['data_admissao'].astype(str)
        
        fig_growth = px.line(
            monthly_hires,
            x='data_admissao',
            y=0,
            title="Contratações por Mês"
        )
        fig_growth.update_layout(yaxis_title="Número de Contratações")
        st.plotly_chart(fig_growth, use_container_width=True)
        
        # Crescimento cumulativo
        cumulative_hires = df_filtered_copy.sort_values('data_admissao')
        cumulative_hires['funcionarios_acumulados'] = range(1, len(cumulative_hires) + 1)
        
        fig_cumulative = px.line(
            cumulative_hires,
            x='data_admissao',
            y='funcionarios_acumulados',
            title="Crescimento Cumulativo de Funcionários"
        )
        st.plotly_chart(fig_cumulative, use_container_width=True)
    
    with tab3:
        st.subheader("Análise por Departamentos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Funcionários por departamento
            dept_count = df_filtered['departamento'].value_counts()
            fig_dept = px.bar(
                x=dept_count.index,
                y=dept_count.values,
                title="Funcionários por Departamento"
            )
            fig_dept.update_xaxes(tickangle=45)
            st.plotly_chart(fig_dept, use_container_width=True)
        
        with col2:
            # Custo por departamento
            dept_cost = df_filtered.groupby('departamento')['salario'].sum().sort_values(ascending=False)
            fig_cost = px.bar(
                x=dept_cost.index,
                y=dept_cost.values,
                title="Custo Total por Departamento"
            )
            fig_cost.update_xaxes(tickangle=45)
            st.plotly_chart(fig_cost, use_container_width=True)
        
        # Tabela resumo por departamento
        dept_summary = df_filtered.groupby('departamento').agg({
            'nome': 'count',
            'salario': ['mean', 'sum']
        }).round(2)
        dept_summary.columns = ['Total Funcionários', 'Salário Médio', 'Custo Total']
        st.subheader("Resumo por Departamento")
        st.dataframe(dept_summary, use_container_width=True)
    
    with tab4:
        st.subheader("Exportar Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Exportar Lista Completa de Funcionários**")
            if st.button("📊 Baixar Excel - Funcionários"):
                excel_data = data_handler.export_to_excel(df_filtered)
                if excel_data:
                    st.download_button(
                        label="⬇️ Download Excel",
                        data=excel_data,
                        file_name=f"funcionarios_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
        
        with col2:
            st.write("**Exportar Relatório de Salários**")
            if st.button("📈 Baixar Relatório de Salários"):
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
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

# Função para configurações
def show_settings():
    st.header("⚙️ Configurações do Sistema")
    
    st.subheader("🔧 Manutenção de Dados")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Backup dos Dados**")
        if st.button("💾 Criar Backup"):
            backup_data = data_handler.create_backup()
            if backup_data:
                st.download_button(
                    label="⬇️ Download Backup",
                    data=backup_data,
                    file_name=f"backup_funcionarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                st.success("✅ Backup criado com sucesso!")
            else:
                st.error("❌ Erro ao criar backup.")
    
    with col2:
        st.write("**Restaurar Dados**")
        uploaded_file = st.file_uploader("Carregar arquivo de backup", type=['csv'])
        if uploaded_file is not None:
            if st.button("🔄 Restaurar Dados"):
                if data_handler.restore_backup(uploaded_file):
                    st.success("✅ Dados restaurados com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao restaurar dados. Verifique o formato do arquivo.")
    
    st.markdown("---")
    
    st.subheader("📊 Informações do Sistema")
    
    df = data_handler.load_data()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Registros", len(df))
    
    with col2:
        if not df.empty:
            last_update = pd.to_datetime(df['data_admissao']).max()
            st.metric("Última Atualização", last_update.strftime('%d/%m/%Y'))
        else:
            st.metric("Última Atualização", "Nunca")
    
    with col3:
        file_size = os.path.getsize(data_handler.data_file) if os.path.exists(data_handler.data_file) else 0
        st.metric("Tamanho do Arquivo", f"{file_size / 1024:.1f} KB")

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
