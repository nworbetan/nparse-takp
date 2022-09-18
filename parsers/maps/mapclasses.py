import datetime

from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPixmap, QPen
from PyQt5.QtWidgets import (QGraphicsItemGroup, QGraphicsLineItem, QGraphicsEllipseItem,
                             QGraphicsPixmapItem, QGraphicsTextItem)

from helpers import format_time, get_degrees_from_line, to_eq_xy, to_real_xy


class MouseLocation(QGraphicsTextItem):
    def __init__(self, **kwargs):
        super().__init__()
        self.setZValue(100)

    def set_value(self, pos, scale, view):
        # pos = QGraphicsView.mapToScale return of mouse event pos()
        # view = QGraphicsView of the scene view
        x, y = to_eq_xy(pos.x(), pos.y())

        self.setHtml(
            "<font color='white' size='4'>{}, {}</font>".format(
                str(int(x)), str(int(y))
            )
        )

        # move hover to left if it goes out of view
        scene_rect = view.mapToScene(view.viewport().rect()).boundingRect()
        visible_x = -(scene_rect.x() + scene_rect.width())
        my_rect = self.mapRectToScene(self.boundingRect())
        if y + -(15/scale + my_rect.width()) < visible_x:
            self.setPos(pos.x() - 15/scale - my_rect.width(), pos.y())
        else:
            self.setPos(pos.x() + 15/scale, pos.y())

        self.setScale(1/scale)


class PointOfInterest:
    def __init__(self, **kwargs):
        super().__init__()
        self.location = MapPoint()
        self.__dict__.update(kwargs)
        self.text = QGraphicsTextItem()
        self.text.setHtml(
            "<font color='{}' size='{}'>{}</font>".format(
                self.location.color.name(),
                1 + self.location.size,
                '\u272a' + self.location.text
            )
        )
        self.text.setZValue(2)
        self.text.setPos(self.location.x, self.location.y)

    def update_(self, scale):
        self.text.setScale(scale)
        self.text.setPos(
            self.location.x - self.text.boundingRect().width() * 0.05 * scale,
            self.location.y - self.text.boundingRect().height() / 2 * scale
        )


class Player(QGraphicsItemGroup):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = ''
        self.location = MapPoint()
        self.previous_location = MapPoint()
        self.timestamp = None  # datetime
        self.scl = 1
        self.__dict__.update(kwargs)
        self.icon = QGraphicsPixmapItem(
            QPixmap('data/maps/user.png')
        )
        self.icon.setOffset(-10, -10)
        self.directional = QGraphicsPixmapItem(
            QPixmap('data/maps/directional.png')
        )
        self.directional.setOffset(-15, -15)
        self.directional.setVisible(False)
        self.addToGroup(self.icon)
        self.addToGroup(self.directional)
        self.setZValue(10)
        self.z_level = 0
        self.setScale(self.scl)

    def update_(self, scale):
        self.setScale(scale)
        if self.previous_location != self.location:
            self.directional.setRotation(
                get_degrees_from_line(
                    self.location.x, self.location.y,
                    self.previous_location.x, self.previous_location.y
                )
            )
            self.directional.setVisible(True)
        self.setPos(self.location.x, self.location.y)


class SpawnPoint(QGraphicsItemGroup):
    def __init__(self, **kwargs):
        super().__init__()
        self.location = MapPoint()
        self.length = 10
        self.name = 'pop'
        self.__dict__.update(**kwargs)
        self.setToolTip(self.name)

        pixmap = QGraphicsPixmapItem(QPixmap('data/maps/spawn.png'))
        text = QGraphicsTextItem('0')

        self.addToGroup(pixmap)
        self.addToGroup(text)
        self.setPos(self.location.x, self.location.y)

        self.setZValue(18)

        self.pixmap = pixmap
        self.text = text

        self.timer = QTimer()

    def _update(self):
        if self.timer:
            remaining = self._end_time - datetime.datetime.now()
            remaining_seconds = remaining.total_seconds()
            if remaining_seconds < 0:
                self.stop()
            elif remaining_seconds <= 30:
                self.text.setHtml(
                    "<font color='red' size='5'>{}</font>".format(
                        format_time(remaining))
                )
            else:
                self.text.setHtml(
                    "<font color='white'>{}</font>".format(
                        format_time(remaining))
                )
            self.realign()

            if remaining_seconds > 0 and self.timer:
                self.timer.singleShot(1000, self._update)

    def realign(self, scale=None):
        if scale:
            self.setPos(self.location.x - self.boundingRect().width() / 2 * scale,
                        self.location.y - self.boundingRect().height() / 2 * scale)
        self.text.setPos(-self.text.boundingRect().width() /
                         2 + self.pixmap.boundingRect().width() / 2, 15)

    def start(self, _=None, timestamp=None):
        timestamp = timestamp if timestamp else datetime.datetime.now()
        self._end_time = timestamp + datetime.timedelta(seconds=self.length)
        if self.timer:
            self._update()

    def stop(self):
        self.text.setHtml(
            "<font color='green' align='center'>{}</font>".format(self.name.upper()))

    def mouseDoubleClickEvent(self, _):
        self.start()


class MapPoint:
    def __init__(self, **kwargs):
        self.x = 0
        self.y = 0
        self.z = 0
        self.color = None  # QColor
        self.size = 0
        self.text = ''
        self.__dict__.update(kwargs)


class WayPoint(QGraphicsItemGroup):
    def __init__(self, **kwargs):
        super().__init__()
        self.start_loc = MapPoint()
        self.end_loc = MapPoint()
        self.__dict__.update(kwargs)

        pixmap = QGraphicsPixmapItem(QPixmap('data/maps/waypoint.png'))
        pixmap.setOffset(-10, -20)
        self.addToGroup(pixmap)
        self.pixmap = pixmap
        self.pixmap.setVisible(True)
        self.pixmap.setZValue(8)

        text = QGraphicsTextItem('0')
        self.addToGroup(text)
        self.text = text
        self.text.setVisible(self.start_loc.x != self.end_loc.x or self.start_loc.y != self.end_loc.y)
        self.text.setZValue(6)

        ch_pen = QPen(Qt.white, 1, Qt.SolidLine)
        self.chh = QGraphicsLineItem(-10, 0, 10, 0)
        self.chh.setPen(ch_pen)
        self.chh.setVisible(True)
        self.chh.setZValue(7)
        self.addToGroup(self.chh)

        self.chv = QGraphicsLineItem(0, -10, 0, 10)
        self.chv.setPen(ch_pen)
        self.chv.setVisible(True)
        self.chv.setZValue(7)
        self.addToGroup(self.chv)

        self.line = QGraphicsLineItem(
            self.start_loc.x, self.start_loc.y, self.end_loc.x, self.end_loc.y)
        self.line.setPen(QPen(
            Qt.green, 1, Qt.DashLine
        ))
        self.line.setVisible(self.start_loc.x != self.end_loc.x or self.start_loc.y != self.end_loc.y)
        self.line.setZValue(4)
        self.setZValue(5)

        self.setPos(self.end_loc.x, self.end_loc.y)
        self.text.setHtml(
            "<body bgcolor='magenta'><font color='white' size='2'>{}</font></body>".format(
            str(int(self.line.line().length())))
        )

    def update_(self, scale, new_start_loc=None):
        self.setScale(scale)
        if new_start_loc:
            self.start_loc.x = new_start_loc.x
            self.start_loc.y = new_start_loc.y
            self.start_loc.z = new_start_loc.z

            line = self.line.line()
            line.setP1(QPointF(self.start_loc.x, self.start_loc.y))
            self.line.setLine(line)
            self.line.setVisible(True)

            self.text.setHtml(
                "<body bgcolor='magenta'><font color='white' size='2'>{}</font></body>".format(
                str(int(line.length())))
            )
            self.text.setVisible(True)


class MapCircle(QGraphicsItemGroup):
    def __init__(self, **kwargs):
        super().__init__()
        self.location = MapPoint()
        self.radius = 0
        self.__dict__.update(kwargs)

        circle = QGraphicsEllipseItem(-self.radius, -self.radius, 2*self.radius, 2*self.radius)
        circle.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
        self.addToGroup(circle)
        self.circle = circle
        self.circle.setVisible(True)

        text = QGraphicsTextItem('0')
        self.addToGroup(text)
        self.text = text
        self.text.setHtml(
            "<body bgcolor='blue'><font color='white' size='2'>{}</font></body>".format(
            str(self.radius))
        )
        self.text.setVisible(True)
        self.text.setZValue(6)

        ch_pen = QPen(Qt.white, 1, Qt.SolidLine)
        self.chh = QGraphicsLineItem(-10, 0, 10, 0)
        self.chh.setPen(ch_pen)
        self.chh.setVisible(True)
        self.chh.setZValue(7)
        self.addToGroup(self.chh)

        self.chv = QGraphicsLineItem(0, -10, 0, 10)
        self.chv.setPen(ch_pen)
        self.chv.setVisible(True)
        self.chv.setZValue(7)
        self.addToGroup(self.chv)

        self.setPos(self.location.x, self.location.y)
        self.setZValue(5)


class MapLine:
    def __init__(self, **kwargs):
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.z1 = 0
        self.color = None  # QColor
        self.__dict__.update(kwargs)


class MapGeometry:
    def __init__(self, **kwargs):
        self.lowest_x = 0
        self.highest_x = 0
        self.lowest_y = 0
        self.highest_y = 0
        self.highest_z = 0
        self.lowest_z = 0
        self.center_x = 0
        self.center_y = 0
        self.width = 0
        self.height = 0
        self.z_groups = []  # [(number:int, count:int)]
        self.__dict__.update(kwargs)
