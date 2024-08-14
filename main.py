from rich import print
from rich.panel import Panel
from rich.console import Console

console = Console()
agenda = {}

def show_contacts():
    if agenda:
        for contato in agenda:
            search_contact(contato)
    else:
        console.print(Panel("Nenhum contato na agenda", style="bold red"))

def search_contact(contato):
    try:
        details = (
            f'Nome: {contato}\n'
            f'Telefone: {agenda[contato]["tel"]}\n'
            f'Email: {agenda[contato]["mail"]}\n'
            f'Endereço: {agenda[contato]["address"]}'
        )
        console.print(Panel(details, title="Contato", style="cyan"))
    except KeyError:
        console.print(Panel("Contato inexistente", style="bold red"))
    except Exception as error:
        console.print(Panel(f'Ocorreu um erro inesperado: {error}', style="bold red"))

def get_details():
    tel = input('Digite o número do telefone: ')
    mail = input('Digite o e-mail: ')
    address = input('Digite o endereço: ')
    return tel, mail, address

def add_update_contact(contato, tel, mail, address):
    agenda[contato] = {
        'tel': tel,
        'mail': mail,
        'address': address,
    }
    save()
    console.print(Panel(f'Contato {contato} adicionado/atualizado com sucesso!', style="green"))

def delete_contact(contato):
    try:
        agenda.pop(contato)
        save()
        console.print(Panel(f'Contato {contato} excluído com SUCESSO!', style="green"))
    except KeyError:
        console.print(Panel(f'Contato {contato} não encontrado!', style="bold red"))
    except Exception as error:
        console.print(Panel(f'Ocorreu um erro inesperado: {error}', style="bold red"))

def export_contacts(file_name):
    try:
        with open(file_name, 'w') as file:
            for name, details in agenda.items():
                tel = details['tel']
                mail = details['mail']
                address = details['address']
                file.write(f'{name},{tel},{mail},{address}\n')
        console.print(Panel('Contatos exportados com sucesso', style="green"))
    except Exception as error:
        console.print(Panel('Ocorreu um erro ao exportar contatos', style="bold red"))
        console.print(error)

def import_contacts(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 4:
                    name, tel, mail, address = parts
                    add_update_contact(name, tel, mail, address)
        console.print(Panel('Contatos importados com sucesso', style="green"))
    except FileNotFoundError:
        console.print(Panel('Arquivo não encontrado', style="bold red"))
    except Exception as error:
        console.print(Panel('Ocorreu um erro inesperado ao importar', style="bold red"))
        console.print(error)

def save():
    export_contacts('database.csv')

def load():
    try:
        with open('database.csv', 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 4:
                    name, tel, mail, address = parts
                    agenda[name] = {
                        'tel': tel,
                        'mail': mail,
                        'address': address,
                    }
        console.print(Panel('Database carregado com sucesso', style="green"))
        console.print(Panel(f'{len(agenda)} contatos carregados', style="cyan"))
    except FileNotFoundError:
        console.print(Panel('Arquivo não encontrado', style="bold red"))
    except Exception as error:
        console.print(Panel('Ocorreu um erro inesperado ao carregar', style="bold red"))
        console.print(error)

def show_menu():
    menu = (
        '1. Listar contatos\n'
        '2. Buscar contato\n'
        '3. Incluir contato\n'
        '4. Editar contato\n'
        '5. Excluir contato\n'
        '6. Exportar para CSV\n'
        '7. Importar contatos CSV\n'
        '0. Sair'
    )
    console.print(Panel(menu, title="Menu", style="blue"))

load()
while True:
    show_menu()
    option = input('Escolha uma opção: ')

    if option == '1':
        show_contacts()

    elif option == '2':
        contato = input("Nome do contato: ")
        search_contact(contato)

    elif option == '3':
        contato = input("Nome do contato: ")
        if contato in agenda:
            console.print(Panel('Contato já existente!', style="bold yellow"))
        else:
            tel, mail, address = get_details()
            add_update_contact(contato, tel, mail, address)

    elif option == '4':
        contato = input("Nome do contato a ser editado: ")
        if contato in agenda:
            console.print(Panel(f'Editando contato: {contato}', style="cyan"))
            tel, mail, address = get_details()
            add_update_contact(contato, tel, mail, address)
        else:
            console.print(Panel('Contato inexistente', style="bold red"))

    elif option == '5':
        contato = input('Nome do contato: ')
        delete_contact(contato)

    elif option == '6':
        file_name = input('Digite o nome do arquivo para exportar: ')
        export_contacts(file_name)

    elif option == '7':
        file_name = input('Digite o nome do arquivo para importar: ')
        import_contacts(file_name)

    elif option == '0':
        console.print(Panel('Até logo!', style="bold green"))
        break
    else:
        console.print(Panel('Opção inválida, escolha 1-7 ou 0 para sair!', style="bold red"))
