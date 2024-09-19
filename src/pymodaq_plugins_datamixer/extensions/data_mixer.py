from qtpy import QtWidgets

from pymodaq_gui import utils as gutils
from pymodaq_utils.config import Config, ConfigError
from pymodaq_utils.logger import set_logger, get_module_name

from pymodaq.utils.config import get_set_preset_path
from pymodaq.extensions.utils import CustomExt


from pymodaq_plugins_datamixer.utils import Config as PluginConfig

logger = set_logger(get_module_name(__file__))

main_config = Config()
plugin_config = PluginConfig()

EXTENSION_NAME = 'Data Mixer'  # the name that will be displayed in the extension list in the
# dashboard
CLASS_NAME = 'DataMixer'  # this should be the name of your class defined below


class DataMixer(CustomExt):
    params = []

    def __init__(self, parent: gutils.DockArea, dashboard):
        super().__init__(parent, dashboard)
        self.setup_ui()

    def setup_docks(self):
        """Mandatory method to be subclassed to setup the docks layout

        Examples
        --------
        >>>self.docks['ADock'] = gutils.Dock('ADock name')
        >>>self.dockarea.addDock(self.docks['ADock'])
        >>>self.docks['AnotherDock'] = gutils.Dock('AnotherDock name')
        >>>self.dockarea.addDock(self.docks['AnotherDock'''], 'bottom', self.docks['ADock'])

        See Also
        --------
        pyqtgraph.dockarea.Dock
        """
        self.docks['settings'] = gutils.Dock('Settings')
        self.dockarea.addDock(self.docks['settings'])
        self.docks['settings'].addWidget(self.settings_tree)

    def setup_actions(self):
        """Method where to create actions to be subclassed. Mandatory

        Examples
        --------
        >>> self.add_action('quit', 'Quit', 'close2', "Quit program")
        >>> self.add_action('grab', 'Grab', 'camera', "Grab from camera", checkable=True)
        >>> self.add_action('load', 'Load', 'Open', "Load target file (.h5, .png, .jpg) or data from camera"
            , checkable=False)
        >>> self.add_action('save', 'Save', 'SaveAs', "Save current data", checkable=False)

        See Also
        --------
        ActionManager.add_action
        """
        pass

    def connect_things(self):
        """Connect actions and/or other widgets signal to methods"""
        pass

    def setup_menu(self):
        """Non mandatory method to be subclassed in order to create a menubar

        create menu for actions contained into the self._actions, for instance:

        Examples
        --------
        >>>file_menu = self.mainwindow.menuBar().addMenu('File')
        >>>self.affect_to('load', file_menu)
        >>>self.affect_to('save', file_menu)

        >>>file_menu.addSeparator()
        >>>self.affect_to('quit', file_menu)

        See Also
        --------
        pymodaq.utils.managers.action_manager.ActionManager
        """
        # todo create and populate menu using actions defined above in self.setup_actions
        pass

    def value_changed(self, param):
        """ Actions to perform when one of the param's value in self.settings is changed from the
        user interface

        For instance:
        if param.name() == 'do_something':
            if param.value():
                print('Do something')
                self.settings.child('main_settings', 'something_done').setValue(False)

        Parameters
        ----------
        param: (Parameter) the parameter whose value just changed
        """
        pass


def main():
    from pymodaq.utils.gui_utils.utils import mkQApp
    from pymodaq.utils.gui_utils.loader_utils import load_dashboard_with_preset
    from pymodaq.utils.messenger import messagebox

    app = mkQApp(EXTENSION_NAME)
    try:
        preset_file_name = plugin_config('presets', f'preset_for_{CLASS_NAME.lower()}')
        load_dashboard_with_preset(preset_file_name, EXTENSION_NAME)
        app.exec()

    except ConfigError as e:
        messagebox(f'No entry with name f"preset_for_{CLASS_NAME.lower()}" has been configured'
                   f'in the plugin config file. The toml entry should be:\n'
                   f'[presets]'
                   f"preset_for_{CLASS_NAME.lower()} = {'a name for an existing preset'}"
                   )


if __name__ == '__main__':
    main()
