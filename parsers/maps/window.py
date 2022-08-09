"""Map parser for nparse."""

from PyQt5.QtWidgets import QHBoxLayout, QPushButton

from helpers import config, to_real_xy, ParserWindow

from .mapcanvas import MapCanvas
from .mapclasses import MapPoint


class Maps(ParserWindow):

    def __init__(self):
        super().__init__()
        self.name = 'maps'
        nameTitle = config.data['general']['eq_charname'] + ' - ' + self.name.title()
        self.setWindowTitle(nameTitle)
        self.set_title(nameTitle)

        # interface
        self._map = MapCanvas()
        self.content.addWidget(self._map, 1)
        # buttons
        button_layout = QHBoxLayout()
        self.use_alt_map = QPushButton('B')
        self.use_alt_map.setCheckable(True)
        self.use_alt_map.setEnabled(False)
        self.use_alt_map.setToolTip('Alternate Map N/A')
        self.use_alt_map.clicked.connect(self._toggle_use_alt_map)
        button_layout.addWidget(self.use_alt_map)
        show_poi = QPushButton('\u272a')
        show_poi.setCheckable(True)
        show_poi.setChecked(config.data['maps']['show_poi'])
        show_poi.setToolTip('Show Points of Interest')
        show_poi.clicked.connect(self._toggle_show_poi)
        button_layout.addWidget(show_poi)
        auto_follow = QPushButton('\u25CE')
        auto_follow.setCheckable(True)
        auto_follow.setChecked(config.data['maps']['auto_follow'])
        auto_follow.setToolTip('Auto Center')
        auto_follow.clicked.connect(self._toggle_auto_follow)
        button_layout.addWidget(auto_follow)
        toggle_z_layers = QPushButton('\u24CF')
        toggle_z_layers.setCheckable(True)
        toggle_z_layers.setChecked(config.data['maps']['use_z_layers'])
        toggle_z_layers.setToolTip('Show Z Layers')
        toggle_z_layers.clicked.connect(self._toggle_z_layers)
        button_layout.addWidget(toggle_z_layers)
        show_grid_lines = QPushButton('#')
        show_grid_lines.setCheckable(True)
        show_grid_lines.setChecked(config.data['maps']['show_grid'])
        show_grid_lines.setToolTip('Show Grid')
        show_grid_lines.clicked.connect(self._toggle_show_grid)
        button_layout.addWidget(show_grid_lines)
        show_mouse_location = QPushButton('\U0001F6C8')
        show_mouse_location.setCheckable(True)
        show_mouse_location.setChecked(config.data['maps']['show_mouse_location'])
        show_mouse_location.setToolTip('Show Loc Under Mouse Pointer')
        show_mouse_location.clicked.connect(self._toggle_show_mouse_location)
        button_layout.addWidget(show_mouse_location)

        self.menu_area.addLayout(button_layout)

        if config.data['maps']['last_zone']:
            self._map.load_map(config.data['maps']['last_zone'])
        else:
            self._map.load_map('west freeport')

    def parse(self, timestamp, text):
        if text[:23] == 'LOADING, PLEASE WAIT...':
            pass
        if text[:16] == 'You have entered':
            mapname = text[17:-1]
            if mapname.replace(" B", "") in ["Plane of Earth", "Plane of Time"]:
                self.use_alt_map.setEnabled(True)
                self.use_alt_map.setToolTip('Alternate Map Available')
            else:
                self.use_alt_map.setEnabled(False)
                self.use_alt_map.setChecked(False)
                self.use_alt_map.setToolTip('Alternate Map N/A')
            self._map.load_map(mapname)
        if text[:16] == 'Your Location is':
            x, y, z = [float(value) for value in text[17:].strip().split(',')]
            x, y = to_real_xy(x, y)
            self._map.add_player('__you__', timestamp, MapPoint(x=x, y=y, z=z))
            self._map.update_()

    # events
    def _toggle_use_alt_map(self, _):
        this_zone = self._map._data.zone
        next_zone = this_zone
        if this_zone in ["Plane of Earth", "Plane of Time"]:
            next_zone = this_zone + " B"
            self.use_alt_map.setChecked(True)
             # switch to "A" here to prepare the button to switch back where we came from
            self.use_alt_map.setToolTip("Switch To \"A\" Map")
        elif this_zone in ["Plane of Earth B", "Plane of Time B"]:
            next_zone = this_zone.replace(" B", "")
            self.use_alt_map.setChecked(False)
             # switch to "B" here to prepare the button to switch back where we came from
            self.use_alt_map.setToolTip("Switch To \"B\" Map")

        if next_zone != this_zone:
            self._map.load_map(next_zone)
            self._map.update_()
    
    def _toggle_show_poi(self, _):
        config.data['maps']['show_poi'] = not config.data['maps']['show_poi']
        config.save()
        self._map.update_()

    def _toggle_auto_follow(self, _):
        config.data['maps']['auto_follow'] = not config.data['maps']['auto_follow']
        config.save()
        self._map.center()

    def _toggle_z_layers(self, _):
        config.data['maps']['use_z_layers'] = not config.data['maps']['use_z_layers']
        config.save()
        self._map.update_()

    def _toggle_show_grid(self, _):
        config.data['maps']['show_grid'] = not config.data['maps']['show_grid']
        config.save()
        self._map.update_()

    def _toggle_show_mouse_location(self, ):
        config.data['maps']['show_mouse_location'] = not config.data['maps']['show_mouse_location']
        config.save()
