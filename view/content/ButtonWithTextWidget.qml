import QtQuick 6.6
import QtQuick.Controls 6.6

RoundButton {
    id: buttonWithTextWidget
    property string title: "Title"
    property int borderRadius: 8
    property alias roundButtonFontweight: buttonWithTextWidget.font.weight
    property alias roundButtonFontpixelSize: buttonWithTextWidget.font.pixelSize
    property alias resp_bgBorderwidth: background.border.width
    width: 194
    height: 44
    implicitWidth: 194
    implicitHeight: 44
    radius: borderRadius
    text: title
    font.pixelSize: 18

    palette.buttonText: buttonWithTextWidget.enabled ? "#F1F2F8" : "#64687E"
    palette.brightText: buttonWithTextWidget.enabled ? "#F1F2F8" : "#64687E"

    font.weight: Font.Medium
    font.family: "Inter"
    background: Rectangle {
        id: background
        radius: borderRadius
        border.color: "#464C6D"
        border.width: 1.5
        color: buttonWithTextWidget.enabled ? buttonWithTextWidget.down ? "#03040A" : "#111428" : "#26293E"
    }
}
