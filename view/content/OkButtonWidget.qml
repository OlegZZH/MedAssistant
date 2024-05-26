import QtQuick 6.6
import QtQuick.Controls 6.6

RoundButton {
    id: okButtonWidget
    property string title: "Title"
    width: 364
    height: 64
    radius: 12
    text: title
    font.pixelSize: 20
    property alias fontWeight: okButtonWidget.font.weight
    property alias fontPixelSize: okButtonWidget.font.pixelSize
    property alias rectangleRadius: rectangle.radius
    property alias rectangleColor: rectangle.color
    property alias textColor: okButtonWidget.palette.buttonText
    font.weight: Font.DemiBold
    palette.buttonText: enabled ? "#FFFFFF" : "#64687E"
    font.family: "Inter"
    background: Rectangle {
        id: rectangle
        color: okButtonWidget.enabled ? okButtonWidget.down ? "#208194" : "#38ADC4" : "#26293E"
        radius: 12
    }
}
