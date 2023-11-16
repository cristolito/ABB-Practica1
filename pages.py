import flet as ft
from datetime import datetime
from catalogo_libros import CatalogoLibros
from libro import Libro

class PageView:
    def __init__(self, page: ft.Page) -> None:
        self.catalogo_libros = CatalogoLibros("catalogo.json")
        self.catalogo_libros.cargar_datos()
        self.page = page
        self.inputs_add_books = {
            "ISBN": ft.TextField(label="ISBN"),
            "titulo": ft.TextField(label="Titulo"),
            "autor": ft.TextField(label="Autor")
        }
        self.search = ft.TextField(label="Búsqueda")
        self.input_delete = ft.TextField(label="Eliminar ISBN")
        self.msg_error = ft.Text()
        self.book = ft.Text()
        self.list_books = ft.Container()
        self.container = ft.Container(padding=ft.padding.all(15),
            margin=ft.margin.only(top=15),
            alignment=ft.alignment.top_center)

    def print(self):
        columna = ft.Column(spacing=7, scroll=ft.ScrollMode.ALWAYS, height=400)
        for libro in self.catalogo_libros.mostrar_catalogo_ordenado():
            columna.controls.append(ft.Container(ft.Text(f'Titulo: "{libro.titulo}, Autor: {libro.autor}", ISBN: {libro.isbn}'), border=ft.border.all(3,"white"), border_radius=ft.border_radius.all(5), padding=ft.padding.all(7), width=600))

        return columna

    def home_page(self):
        container = ft.Container(ft.Column([
                ft.Text("¡Bienvenido a Alenjandría!"),
                ft.Text(f"Día {datetime.now().date().day} del mes {datetime.now().date().month} de {datetime.now().date().year}"),
                self.print()
            ]),
            padding=ft.padding.all(15),
            margin=ft.margin.all(0),
            alignment=ft.alignment.top_center
        )

        return container
    
    def handle_add_submit(self, e):
        self.msg_error.value = ""
        self.book.value = ""
        isbn = self.inputs_add_books["ISBN"].value
        titulo = self.inputs_add_books["titulo"].value
        autor = self.inputs_add_books["ISBN"].value

        if isbn != "" and titulo != "" and autor != "":
            self.catalogo_libros.insertar_libro(Libro(isbn,titulo,autor))
            self.book.value = f"ISBN: {isbn} - Titulo {titulo} - Autor{autor}"
            self.catalogo_libros.guardar_datos()
            self.container.content.controls.pop()
            list_books = self.print()
            list_books.height = 200
            self.container.content.controls.append(list_books)
        else:
            self.msg_error.value = "Llena todos los campos"
        self.page.update()

    def add_book(self):
        self.msg_error.value = ""
        self.book.value = ""
        self.container.content = ft.Column([
                ft.Text("Registro de libros"),
                self.book
            ])

        for index, item in self.inputs_add_books.items():
            self.container.content.controls.append(item)
            item.value = ""

        btn_submit = ft.ElevatedButton("Enviar", on_click=self.handle_add_submit)
        self.container.content.controls.append(btn_submit)
        self.container.content.controls.append(self.msg_error)
        list_books = self.print()
        list_books.height = 200
        self.container.content.controls.append(list_books)

        return self.container

    def delete_book(self):
        self.msg_error.value = ""
        self.input_delete.value = ""
        container = ft.Container(ft.Column([
                ft.Text("Eliminar libros"),
                self.input_delete
            ]),
            padding=ft.padding.all(15),
            margin=ft.margin.only(top=15),
            alignment=ft.alignment.top_center
        )

        return container
    
    def handle_delete(self, e):
        self.msg_error.value = ""
        self.book.value = ""
        if self.input_delete.value != "":
            self.catalogo_libros.eliminar_libro(self.input_delete.value)
            self.catalogo_libros.guardar_datos()
            list_books = self.print()
            list_books.height = 200
            self.container.content.controls.pop()
            self.container.content.controls.append(ft.Container(list_books))
            self.input_delete.value = ""
        else:
            self.msg_error.value = "Llena el campo"
        self.page.update()
    
    def delete_book(self):
        self.msg_error.value = ""
        self.book.value = ""
        self.input_delete.value = ""
        
        self.container.content = ft.Text("No hay pacientes registrados")
        btn_submit = ft.ElevatedButton("Eliminar", on_click=self.handle_delete)
        if self.catalogo_libros.mostrar_catalogo_ordenado():
            list_books = self.print()
            list_books.height = 300
            self.container.content = ft.Column([
                ft.Text("Eliminar libros"),
                self.input_delete, btn_submit, self.msg_error, self.book,
                ft.Container(list_books)
            ]
        )

        return self.container
        