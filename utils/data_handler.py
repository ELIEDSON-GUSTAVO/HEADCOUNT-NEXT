import pandas as pd
import os
from datetime import datetime
import io

class DataHandler:
    def __init__(self):
        self.data_file = "data/funcionarios.csv"
        self.ensure_data_directory()
        self.ensure_data_file()
    
    def ensure_data_directory(self):
        """Garante que o diretório data existe"""
        os.makedirs("data", exist_ok=True)
    
    def ensure_data_file(self):
        """Garante que o arquivo CSV existe com as colunas corretas"""
        if not os.path.exists(self.data_file):
            columns = ['nome', 'email', 'telefone', 'departamento', 'cargo', 
                      'salario', 'data_admissao', 'status', 'observacoes']
            df = pd.DataFrame(columns=columns)
            df.to_csv(self.data_file, index=False)
    
    def load_data(self):
        """Carrega os dados do arquivo CSV"""
        try:
            if os.path.exists(self.data_file):
                df = pd.read_csv(self.data_file)
                if df.empty:
                    columns = ['nome', 'email', 'telefone', 'departamento', 'cargo', 
                              'salario', 'data_admissao', 'status', 'observacoes']
                    return pd.DataFrame(columns=columns)
                return df
            else:
                columns = ['nome', 'email', 'telefone', 'departamento', 'cargo', 
                          'salario', 'data_admissao', 'status', 'observacoes']
                return pd.DataFrame(columns=columns)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            columns = ['nome', 'email', 'telefone', 'departamento', 'cargo', 
                      'salario', 'data_admissao', 'status', 'observacoes']
            return pd.DataFrame(columns=columns)
    
    def save_data(self, df):
        """Salva os dados no arquivo CSV"""
        try:
            df.to_csv(self.data_file, index=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False
    
    def add_employee(self, employee_data):
        """Adiciona um novo funcionário"""
        try:
            df = self.load_data()
            
            # Verificar se o email já existe
            if not df.empty and employee_data['email'] in df['email'].values:
                return False
            
            # Adicionar novo funcionário
            new_employee = pd.DataFrame([employee_data])
            df = pd.concat([df, new_employee], ignore_index=True)
            
            return self.save_data(df)
        except Exception as e:
            print(f"Erro ao adicionar funcionário: {e}")
            return False
    
    def update_employee(self, email, updated_data):
        """Atualiza um funcionário existente"""
        try:
            df = self.load_data()
            
            if df.empty:
                return False
            
            # Encontrar o índice do funcionário
            employee_index = df[df['email'] == email].index
            
            if len(employee_index) == 0:
                return False
            
            # Atualizar os dados
            for key, value in updated_data.items():
                df.loc[employee_index[0], key] = value
            
            return self.save_data(df)
        except Exception as e:
            print(f"Erro ao atualizar funcionário: {e}")
            return False
    
    def delete_employee(self, email):
        """Exclui um funcionário"""
        try:
            df = self.load_data()
            
            if df.empty:
                return False
            
            # Remover o funcionário
            df = df[df['email'] != email]
            
            return self.save_data(df)
        except Exception as e:
            print(f"Erro ao excluir funcionário: {e}")
            return False
    
    def export_to_excel(self, df):
        """Exporta dados para Excel"""
        try:
            output = io.BytesIO()
            
            # Usar o BytesIO diretamente como buffer
            with pd.ExcelWriter(output, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, sheet_name='Funcionários', index=False)
                
                # Formatação básica
                if 'Funcionários' in writer.sheets:
                    worksheet = writer.sheets['Funcionários']
                    
                    # Ajustar largura das colunas
                    for idx, col in enumerate(df.columns):
                        if not df.empty:
                            max_length = max(
                                df[col].astype(str).apply(len).max(),
                                len(col)
                            )
                            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
            
            output.seek(0)
            return output.getvalue()
        except Exception as e:
            print(f"Erro ao exportar para Excel: {e}")
            return None
    
    def export_salary_report(self, salary_data):
        """Exporta relatório de salários para Excel"""
        try:
            output = io.BytesIO()
            
            # Usar o BytesIO diretamente como buffer
            with pd.ExcelWriter(output, engine='openpyxl', mode='w') as writer:
                salary_data.to_excel(writer, sheet_name='Relatório de Salários')
                
                # Formatação básica
                if 'Relatório de Salários' in writer.sheets:
                    worksheet = writer.sheets['Relatório de Salários']
                    
                    # Ajustar largura das colunas
                    for idx in range(len(salary_data.columns) + 1):
                        worksheet.column_dimensions[chr(65 + idx)].width = 20
            
            output.seek(0)
            return output.getvalue()
        except Exception as e:
            print(f"Erro ao exportar relatório: {e}")
            return None
    
    def create_backup(self):
        """Cria um backup dos dados"""
        try:
            df = self.load_data()
            
            if df.empty:
                return None
            
            output = io.StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return output.getvalue()
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
            return None
    
    def restore_backup(self, uploaded_file):
        """Restaura dados de um arquivo de backup"""
        try:
            # Ler o arquivo carregado
            df = pd.read_csv(uploaded_file)
            
            # Verificar se possui as colunas necessárias
            required_columns = [
                'nome', 'email', 'telefone', 'departamento', 'cargo', 
                'salario', 'data_admissao', 'status', 'observacoes'
            ]
            
            if not all(col in df.columns for col in required_columns):
                return False
            
            # Salvar os dados restaurados
            return self.save_data(df)
        except Exception as e:
            print(f"Erro ao restaurar backup: {e}")
            return False
    
    def get_statistics(self):
        """Retorna estatísticas básicas dos dados"""
        try:
            df = self.load_data()
            
            if df.empty:
                return {
                    'total_employees': 0,
                    'total_salary': 0,
                    'avg_salary': 0,
                    'departments': 0
                }
            
            return {
                'total_employees': len(df),
                'total_salary': df['salario'].sum(),
                'avg_salary': df['salario'].mean(),
                'departments': df['departamento'].nunique()
            }
        except Exception as e:
            print(f"Erro ao calcular estatísticas: {e}")
            return {
                'total_employees': 0,
                'total_salary': 0,
                'avg_salary': 0,
                'departments': 0
            }
