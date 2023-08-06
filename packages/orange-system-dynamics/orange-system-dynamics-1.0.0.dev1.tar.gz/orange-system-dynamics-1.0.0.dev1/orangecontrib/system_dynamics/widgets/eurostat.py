from Orange.widgets import widget, gui, settings
from Orange.widgets.widget import Output
from Orange.data import Table
from pandas.core.frame import DataFrame
from drb.drivers.eurostat import DrbEurostatFactory
from Orange.data.pandas_compat import table_from_frame


class OWEurostat(widget.OWWidget):
    name = "Eurostat"
    description = "Access and retrieve data from Eurostat service"
    icon = "icons/eurostat.svg"
    priority = 30
    variables = []
    codes = []
    want_main_area = False
    graph_name = "thumbnailView"
    auto_commit = settings.Setting(True)

    class Outputs:
        output = Output("Data", Table)

    def __init__(self):
        super().__init__()
        self.service = None
        self.output = None

        box = gui.widgetBox(self.controlArea,
                            box="Enter a keyword (ex: population):")
        self.search_line = gui.lineEdit(box, self, "", controlWidth=400)

        self.button = gui.button(
            box, self, "Query Service",
            autoDefault=False,
            callback=self.query_service
        )

        gui.rubber(self.controlArea)
        self.combobox = gui.comboBox(
            self.controlArea, self, "", items=self.variables,
            box="Select Variable:",
            contentsLength=8,
        )
        self.combobox.activated.connect(self.load_variable)

        gui.rubber(self.controlArea)
        gui.auto_commit(self.buttonsArea, self, "auto_commit", "Send",
                        box=False)

    def query_service(self):

        factory = DrbEurostatFactory()
        self.service = factory.create('eurostat://')

        tables = self.service.get_attribute('tables')
        search = self.search_line.text()
        self.search_line.clear()

        self.variables = []
        self.codes = []

        for table in tables:
            if search in table[0].lower():

                self.variables.append(table[0])
                self.codes.append(table[1])

        self.combobox.clear()
        self.combobox.addItems([var for var in self.variables])

    def load_variable(self):
        idx = self.combobox.currentIndex()
        code = self.codes[idx]
        table = self.service[code]
        df = table.get_impl(DataFrame)

        self.output = table_from_frame(df)
        self.commit.deferred()

    @gui.deferred
    def commit(self):
        """
        Commits the result the next widget in the line.
        """
        if self.output:
            self.Outputs.output.send(self.output)

        else:
            self.Outputs.output.send(None)


if __name__ == "__main__":
    from orangewidget.utils.widgetpreview import WidgetPreview
    WidgetPreview(OWEurostat).run()
