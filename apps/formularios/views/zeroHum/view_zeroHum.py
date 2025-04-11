import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
import pytz
from django.contrib import messages
import pandas as pd
from django.core.files.storage import FileSystemStorage


def get_timestamp():
    brazil_tz = pytz.timezone('America/Sao_Paulo')
    brazil_now = timezone.now().astimezone(brazil_tz)
    return brazil_now.strftime('ZEROHUM'+'%d-%m-%Y_%H-%M-%S')

def create_upload_directory(timestamp):
    upload_path = os.path.join('uploads', timestamp)
    os.makedirs(upload_path, exist_ok=True)
    return upload_path

def formZeroHum(request):
    print("Entrou na view formulario_rapido")

    if request.method == 'POST':
        print("Recebendo um POST request...")
        print("Dados do formulário (POST):", request.POST)
        print("Arquivos enviados (FILES):", request.FILES)

        # Validação manual dos campos obrigatórios
        titulo = request.POST.get('titulo')
        data_entrega = request.POST.get('dataEntrega')
        files = request.FILES.getlist('file')

        if not titulo or not data_entrega or not files:
            print("Erro: Campos obrigatórios ausentes")
            return JsonResponse({'error': 'Campos obrigatórios ausentes'}, status=400)

        timestamp = get_timestamp()
        upload_path = create_upload_directory(timestamp)

        uploaded_files = []

        for file in files:
            file_path = os.path.join(upload_path, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            uploaded_files.append(file.name)

            # Criar e salvar os metadados do upload em um JSON
            json_data = {
                'nomeArquivo': file.name,
                'caminho': file_path,
                'numeroArquivos': len(files),
                'nomeUnidade': {
                    'ARARUAMA': int(request.POST.get('ARARUAMA', 0) or 0),
                    'CABO_FRIO': int(request.POST.get('CABO_FRIO', 0) or 0),
                    'ITABORAI': int(request.POST.get('ITABORAI', 0) or 0),
                    'ITAIPUACU': int(request.POST.get('ITAIPUACU', 0) or 0),
                    'MARICA_I': int(request.POST.get('MARICA_I', 0) or 0),
                    'NOVA_FRIBURGO': int(request.POST.get('NOVA_FRIBURGO', 0) or 0),
                    'QUEIMADOS': int(request.POST.get('QUEIMADOS', 0) or 0),
                    'SEROPEDICA': int(request.POST.get('SEROPEDICA', 0) or 0),
                    'ALCANTARA': int(request.POST.get('ALCANTARA', 0) or 0),
                    'BANGU': int(request.POST.get('BANGU', 0) or 0),
                    'BARRA_DA_TIJUCA': int(request.POST.get('BARRA_DA_TIJUCA', 0) or 0),
                    'BELFORD_ROXO': int(request.POST.get('BELFORD_ROXO', 0) or 0),
                    'DUQUE_DE_CAXIAS': int(request.POST.get('DUQUE_DE_CAXIAS', 0) or 0),
                    'ICARAI': int(request.POST.get('ICARAI', 0) or 0),
                    'ILHA_DO_GOVERNADOR': int(request.POST.get('ILHA_DO_GOVERNADOR', 0) or 0),
                    'ITAIPU': int(request.POST.get('ITAIPU', 0) or 0),
                    'MADUREIRA': int(request.POST.get('MADUREIRA', 0) or 0),
                    'MEIER': int(request.POST.get('MEIER', 0) or 0),
                    'NILOPOLIS': int(request.POST.get('NILOPOLIS', 0) or 0),
                    'NITEROI': int(request.POST.get('NITEROI', 0) or 0),
                    'NOVA_IGUACU': int(request.POST.get('NOVA_IGUACU', 0) or 0),
                    'OLARIA': int(request.POST.get('OLARIA', 0) or 0),
                    'PRATA': int(request.POST.get('PRATA', 0) or 0),
                    'SAO_GONCALO': int(request.POST.get('SAO_GONCALO', 0) or 0),
                    'SAO_JOAO_DE_MERITI': int(request.POST.get('SAO_JOAO_DE_MERITI', 0) or 0),
                    'VILA_ISABEL': int(request.POST.get('VILA_ISABEL', 0) or 0),
                    'VILAR_DOS_TELES': int(request.POST.get('VILAR_DOS_TELES', 0) or 0),
                },
                'dadosFormulario': {
                    'titulo': titulo,
                    'dataEntrega': data_entrega,
                    'observacoes': request.POST.get('observacoes'),
                    'formato': request.POST.get('formato'),
                    'corImpressao': request.POST.get('corImpressao'),
                    'impressao': request.POST.get('impressao'),
                    'gramatura': request.POST.get('gramatura'),
                    'papelAdesivo': None,
                    'tipoAdesivo': request.POST.get('tipoAdesivo') if request.POST.get('papelAdesivo') == 'sim' else None,
                    'grampos': request.POST.get('grampos'),
                    'espiral': None,
                    'capaPVC': request.POST.get('capaPVC'),
                    'contato': {
                        'nome': request.POST.get('nome'),
                        'email': request.POST.get('email'),
                    }
                },
                'timestamp': timestamp
            }

            json_file_path = os.path.join(upload_path, f"{os.path.splitext(file.name)[0]}.json")
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        print(f"Upload concluído! {len(uploaded_files)} arquivos salvos.")

        return JsonResponse({
            'message': 'Upload concluído com sucesso!',
            'arquivos': uploaded_files
        })


    return render(request, 'formularios/zeroHumForm/formRapido.html')

def formZeroHumEx(request):
    print("Entrou na view formulario_rapido_excel")
    
    if request.method == 'POST':
        print("Recebendo um POST request...")
        print("Dados do formulário (POST):", request.POST)
        print("Arquivos enviados (FILES):", request.FILES)

        files = request.FILES.getlist('file')
        if not files:
            print("Erro: Nenhum arquivo PDF enviado")
            return JsonResponse({'error': 'Nenhum arquivo PDF enviado'}, status=400)

        excel_file = request.FILES.get("excel_file")
        print("Arquivo Excel:", excel_file)
        if not excel_file:
            print("Erro: Nenhum arquivo Excel enviado")
            return JsonResponse({'error': 'Nenhum arquivo Excel enviado'}, status=400)

        timestamp = get_timestamp()
        upload_path = create_upload_directory(timestamp)
        os.makedirs(upload_path, exist_ok=True)

        # Salvando o Excel
        excel_path = os.path.join(upload_path, excel_file.name)
        with open(excel_path, 'wb+') as destination:
            for chunk in excel_file.chunks():
                destination.write(chunk)

        # Lendo a aba 'PEDIDO' do Excel
        df_pedido = pd.read_excel(excel_path, sheet_name='PEDIDO')
        df_pedido = df_pedido.dropna(subset=["UNIDADES"])
        df_pedido['UNIDADES'] = df_pedido['UNIDADES'].str.strip()

        # Lista padrão de unidades
        lista_unidades = [
            'ARARUAMA', 'CABO_FRIO', 'ITABORAI', 'ITAIPUACU', 'MARICA_I', 'NOVA_FRIBURGO',
            'QUEIMADOS', 'SEROPEDICA', 'ALCANTARA', 'BANGU', 'BARRA_DA_TIJUCA',
            'BELFORD_ROXO', 'DUQUE_DE_CAXIAS', 'ICARAI', 'ILHA_DO_GOVERNADOR', 'ITAIPU',
            'MADUREIRA', 'MEIER', 'NILOPOLIS', 'NITEROI', 'NOVA_IGUACU', 'OLARIA',
            'PRATA', 'SAO_GONCALO', 'SAO_JOAO_DE_MERITI', 'VILA_ISABEL', 'VILAR_DOS_TELES'
        ]

        # Criando dicionário nomeUnidade corretamente
        nome_unidade_dict = {}
        for unidade in lista_unidades:
            linha = df_pedido[df_pedido['UNIDADES'].str.upper() == unidade]
            if not linha.empty:
                valor = linha['QTDE'].values[0]
                # Verifica se o valor é um número e não é NaN
                if pd.notna(valor):
                    nome_unidade_dict[unidade] = float(valor)
                else:
                    nome_unidade_dict[unidade] = None
            else:
                nome_unidade_dict[unidade] = None


        uploaded_files = []
        for file in files:
            pdf_path = os.path.join(upload_path, file.name)
            with open(pdf_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            uploaded_files.append(file.name)

            json_filename = os.path.splitext(file.name)[0] + ".json"
            json_path = os.path.join(upload_path, json_filename)

            json_data = {
                'nomeArquivo': file.name,
                'caminho': pdf_path,
                'numeroArquivos': len(files),
                'nomeUnidade': nome_unidade_dict,
                'codigoDeSaida': 'teste',
                'dadosFormulario': {
                    'titulo': request.POST.get('titulo'),
                    'dataEntrega': request.POST.get('dataEntrega'),
                    'observacoes': request.POST.get('observacoes'),
                    'formato': request.POST.get('formato'),
                    'corImpressao': request.POST.get('corImpressao'),
                    'impressao': request.POST.get('impressao'),
                    'gramatura': request.POST.get('gramatura'),
                    'papelAdesivo': request.POST.get('papelAdesivo'),
                    'tipoAdesivo': request.POST.get('tipoAdesivo') if request.POST.get('papelAdesivo') == 'sim' else None,
                    'grampos': request.POST.get('grampos'),
                    'espiral': None,
                    'capaPVC': request.POST.get('capaPVC'),
                    'contato': {
                        'nome': request.POST.get('nome'),
                        'email': request.POST.get('email'),
                    }
                },
                'timestamp': timestamp
            }

            with open(json_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        print(f"Upload concluído! {len(uploaded_files)} arquivos salvos.")
        return JsonResponse({
            'message': 'Upload concluído com sucesso!',
            'arquivos': uploaded_files,
            'numeroArquivos': len(uploaded_files)
        })

    return render(request, 'formularios/zeroHumForm/formRapidoExcel.html')


