import webbrowser


class Start:
    """Class for starting the default web browser and loading a specified HTML file."""

    def __init__(self, page='index.html'):
        """
        Constructor for Start class.

        Args:
            page (str): The path to the HTML file to load.
        """
        self.page = page

    def open_page(self):
        """Open the default web browser and load the specified HTML file."""
        try:
            webbrowser.open(self.page)
            print("Page loaded successfully.")
        except Exception as e:
            print(f"Error loading page: {str(e)}")


class Renderer:
    """Class for rendering HTML templates with dynamic data."""

    def __init__(self, template_file):
        """
        Constructor for Renderer class.

        Args:
            template_file (str): The path to the HTML template file.
        """
        self.template_file = template_file

    def render(self, context):
        """
        Render the HTML template with dynamic data.

        Args:
            context (dict): A dictionary of key-value pairs representing the data to include in the template.

        Returns:
            str: The rendered HTML code.
        """
        with open(self.template_file, 'r') as f:
            template = f.read()

        # Replace placeholders in the template with values from the context
        for key, value in context.items():
            placeholder = '{{ %s }}' % key
            template = template.replace(placeholder, str(value))

        return template
