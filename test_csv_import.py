import pandas as pd

# Teste do processamento CSV
def test_csv_processing():
    try:
        # Tentar diferentes separadores e encodings
        try:
            df = pd.read_csv('data/teste_import.csv', sep=';', encoding='utf-8')
        except:
            try:
                df = pd.read_csv('data/teste_import.csv', sep=';', encoding='latin-1')
            except:
                df = pd.read_csv('data/teste_import.csv', sep=',', encoding='utf-8')
        
        print("Arquivo lido com sucesso!")
        print(f"Colunas encontradas: {list(df.columns)}")
        print(f"Número de funcionários: {len(df)}")
        
        # Limpar nomes das colunas
        df.columns = df.columns.str.strip()
        
        # Mapear colunas com nomes alternativos
        column_mapping = {
            'data admissao': 'data_admissao',
            'data_admissao': 'data_admissao',
            'salario': 'salario',
            ' salario ': 'salario'
        }
        
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        print(f"Colunas após limpeza: {list(df.columns)}")
        
        # Verificar algumas conversões
        for index, row in df.head(3).iterrows():
            print(f"\nFuncionário {index + 1}:")
            print(f"  Nome: {row['nome']}")
            print(f"  Cargo: {row['cargo']}")
            
            # Testar conversão de salário
            salario_str = str(row['salario']).strip()
            salario_clean = salario_str.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
            try:
                salario_value = float(salario_clean)
                print(f"  Salário original: {row['salario']} -> Convertido: {salario_value}")
            except:
                print(f"  Erro na conversão do salário: {row['salario']}")
            
            # Testar conversão de data
            data_str = str(row['data_admissao']).strip()
            if '/' in data_str:
                parts = data_str.split('/')
                if len(parts) == 3:
                    data_formatted = f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
                    print(f"  Data original: {row['data_admissao']} -> Convertida: {data_formatted}")
                else:
                    print(f"  Data não convertida: {row['data_admissao']}")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_csv_processing()