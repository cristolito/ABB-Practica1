import flet as ft
from pages import PageView
from navigation_bar import NavigationBar

def main(page: ft.Page):
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(
                            leading_width=40,
                            title=ft.Text("Librería Alejandrina"),
                            center_title=False,
                            bgcolor=ft.colors.SURFACE_VARIANT,
                        ),
                        ft.Row([
                            navigation_bar,
                            ft.Column([page_view.home_page()],expand=True)
                        ])
                    ],
                )
            )
        if page.route == "/addbook":
            page.views.append(
                ft.View(
                    "/addbook",
                    [
                        ft.AppBar(
                            leading_width=40,
                            title=ft.Text("Registro de Libros"),
                            center_title=False,
                            bgcolor=ft.colors.SURFACE_VARIANT,
                        ),
                        ft.Row([
                            navigation_bar,
                            ft.Column([page_view.add_book()],expand=True)
                        ],expand=True)
                    ],
                )
            )
        if page.route == "/deletebook":
            page.views.append(
                ft.View(
                    "/deletebook",
                    [
                        ft.AppBar(
                            leading_width=40,
                            title=ft.Text("Eliminar un Libro"),
                            center_title=False,
                            bgcolor=ft.colors.SURFACE_VARIANT,
                        ),
                        ft.Row([
                            navigation_bar,
                            ft.Column([page_view.delete_book()],expand=True)
                        ],expand=True)
                    ],
                )
            )
        page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    routes = [
        "/",
        "/addbook",
        "/deletebook"
    ]

    navigation_bar = NavigationBar(page, routes).build_navigation_bar()
    page_view = PageView(page)
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)

ft.app(target=main)