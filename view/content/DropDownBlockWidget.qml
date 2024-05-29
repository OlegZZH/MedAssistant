import QtQuick 6.6
import QtQuick.Controls 6.6
import QtQuick.Layouts

Rectangle {
    id: dropDownWidget
    width: 676
    height: 60
    color: "#111428"
    radius: 4
    border.color: "#464C6D"
    border.width: 2
    property alias cholesterolLevelFieldWidget: cholesterolLevelFieldWidget
    property alias bloodPressureFieldWidget: bloodPressureFieldWidget
    property alias sexFieldWidget: sexFieldWidget
    property string disease: ""
    property alias difficultyBreathingCheckBoxWidgetChecked: difficultyBreathingCheckBoxWidget.checked
    property alias fatigueCheckBoxWidgetChecked: fatigueCheckBoxWidget.checked
    property alias coughCheckBoxWidgetChecked: coughCheckBoxWidget.checked
    property alias feverCheckBoxWidgetChecked: feverCheckBoxWidget.checked
    property alias ageFieldWidgetInputText: ageFieldWidget.inputText
    property string titleText: "Text"
    property bool checkable: false
    property bool checked: false
    clip: true
    property bool enabled: true
    property int fullSizeHeight: 400

    Text {
        id: name
        text: qsTr(`${dropDownWidget.titleText} :`)
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 20
        anchors.topMargin: 20
        font.pixelSize: 20
        color: dropDownWidget.enabled ? "#F1F2F8" : "#64687E"
    }
    Text {
        id: disease
        text: qsTr(`${dropDownWidget.disease}`)
        anchors.left: name.right
        anchors.top: parent.top
        anchors.leftMargin: 8
        anchors.topMargin: 20
        font.pixelSize: 20
        color: text === "Healthy" ? "#268428" : "#A00606"
    }

    Image {
        id: image
        width: 20
        height: 20
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: 20
        anchors.bottomMargin: 20
        source: {
            if (checkable) {
                if (checked) {
                    return "images/checked.svg"
                } else {
                    return "images/unchecked.svg"
                }
            } else {
                return "images/chevron.svg"
            }
        }
        rotation: checkable ? 0 : 90
        opacity: dropDownWidget.enabled ? 1 : 0.5
        fillMode: Image.PreserveAspectFit
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        enabled: dropDownWidget.enabled
        onClicked: checkable ? selectFunct() : openFunct()
        function selectFunct() {
            checked = !checked
        }
        function openFunct() {
            if (dropDownWidget.state === "") {
                dropDownWidget.state = "opened"
            } else {
                dropDownWidget.state = ""
            }
        }
    }

    Item {
        id: content
        anchors.fill: parent
        Text {
            id: patientTitle
            color: "#ffffff"
            text: qsTr("Patient")
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 40
            anchors.topMargin: 60
            font.pixelSize: 18
        }

        Rectangle {
            id: rectangle
            height: 2
            color: "#62667a"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: patientTitle.bottom
            anchors.leftMargin: 40
            anchors.rightMargin: 40
            anchors.topMargin: 6
        }

        InputFieldWidget {
            id: nameFieldWidget
            x: 40
            width: 160
            height: 64
            anchors.top: rectangle.bottom
            anchors.topMargin: 6
            placeholderText: "Patient Name"
            inputText: dropDownWidget.titleText
            enabled: false
            inputHints: Qt.ImhPreferUppercase
        }

        InputFieldWidget {
            id: ageFieldWidget
            width: 98
            height: 64
            anchors.left: nameFieldWidget.right
            anchors.top: rectangle.bottom
            anchors.leftMargin: 6
            anchors.topMargin: 6
            placeholderText: "Age"
            inputText: ""
            enabled: false
            inputHints: Qt.ImhDigitsOnly
            fieldName: "Age"
        }

        ComboFieldWidget {
            id: sexFieldWidget
            width: 230
            height: 64
            anchors.left: ageFieldWidget.right
            anchors.top: rectangle.bottom
            anchors.leftMargin: 6
            anchors.topMargin: 6
            fieldTitle: "Sex"
            current: -1
            enabled: false
            comboModel: ["Male", "Female"]
        }

        Text {
            id: symptomsTitle
            color: "#ffffff"
            text: qsTr("Symptoms")
            anchors.left: parent.left
            anchors.top: nameFieldWidget.bottom
            anchors.leftMargin: 40
            anchors.topMargin: 16
            font.pixelSize: 18
        }

        Rectangle {
            id: rectangle1
            height: 2
            color: "#62667a"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: symptomsTitle.bottom
            anchors.leftMargin: 40
            anchors.rightMargin: 40
            anchors.topMargin: 6
        }

        GridLayout {
            id: grid
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: rectangle1.bottom
            anchors.leftMargin: 40
            anchors.rightMargin: 40
            anchors.topMargin: 6
            CheckBoxWidget {
                id: feverCheckBoxWidget
                text: "Fever"
                enabled: false
            }

            CheckBoxWidget {
                id: coughCheckBoxWidget
                text: "Cough"
                enabled: false
            }

            CheckBoxWidget {
                id: fatigueCheckBoxWidget
                text: "Fatigue"
                enabled: false
            }

            CheckBoxWidget {
                id: difficultyBreathingCheckBoxWidget
                text: "Difficulty Breathing"
                enabled: false
            }
        }

        ComboFieldWidget {
            id: bloodPressureFieldWidget
            height: 64
            anchors.left: parent.left
            anchors.right: parent.horizontalCenter
            anchors.top: grid.bottom
            anchors.leftMargin: 40
            anchors.rightMargin: 10
            anchors.topMargin: 12
            fieldTitle: "Blood Pressure"
            current: 0
            comboModel: ["Normal", "Low", "High"]
            enabled: false
        }

        ComboFieldWidget {
            id: cholesterolLevelFieldWidget
            height: 64
            anchors.left: parent.horizontalCenter
            anchors.right: parent.right
            anchors.top: grid.bottom
            anchors.leftMargin: 10
            anchors.rightMargin: 40
            anchors.topMargin: 12
            fieldTitle: "Cholesterol Level"
            current: 0
            comboModel: ["Normal", "Low", "High"]
            enabled: false
        }
    }
    states: [
        State {
            name: "opened"

            PropertyChanges {
                target: image
                rotation: -90
            }
            PropertyChanges {
                target: dropDownWidget
                height: dropDownWidget.fullSizeHeight
            }
            PropertyChanges {
                target: mouseArea
                anchors.leftMargin: dropDownWidget.width - 60
                anchors.topMargin: dropDownWidget.fullSizeHeight - 60
            }
            PropertyChanges {
                target: content
                opacity: 1
                enabled: true
            }
        }
    ]
    transitions: Transition {
        reversible: true
        NumberAnimation {

            properties: "height,rotation,opacity"
            duration: 500
            easing.type: Easing.InOutQuad
        }
    }
    onCheckableChanged: {
        if (checkable && state !== "") {
            state = ""
        }
    }
}
