from pages.login_page import LoginPage

class PageFactory:

    @staticmethod
    def get_page(context, page_name: str):
        pages = {
            "LoginPage": LoginPage
        }

        if page_name not in pages:
            raise Exception(f"Page {page_name} not found")

        return pages[page_name](context)
