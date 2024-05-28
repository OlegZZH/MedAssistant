import QtQuick 6.6
import QtQuick.Layouts

ModalWindowFrame {
    id: modalWindowFrame
    width: 580
    height: 550

    implicitWidth: 580
    implicitHeight: 550

    Text {
        id: mainTitle
        color: "#ffffff"
        text: qsTr("Adding a patient")
        anchors.top: parent.top
        anchors.topMargin: 72
        font.pixelSize: 24
        anchors.horizontalCenter: parent.horizontalCenter
    }

    ButtonWithTextWidget {
        id: buttonWithTextWidget
        y: 367
        height: 60
        text: "Close"
        anchors.left: parent.left
        anchors.right: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.leftMargin: 40
        anchors.rightMargin: 10
        anchors.bottomMargin: 40
        borderRadius: 12
        onClicked: {
            addPatientDialog.close()
        }
    }

    OkButtonWidget {
        id: okButtonWidget
        y: 367
        text: "Add"
        enabled: nameFieldWidget.inputText !== "" && ageFieldWidget.inputText !== "" && sexFieldWidget.current
                 !== -1 && ageFieldWidget.acceptableInput
                 && (feverCheckBoxWidget.checked || coughCheckBoxWidget.checked
                     || fatigueCheckBoxWidget.checked || difficultyBreathingCheckBoxWidget.checked
                     || bloodPressureFieldWidget.current > 0 || cholesterolLevelFieldWidget.current > 0)
        anchors.left: parent.horizontalCenter
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.leftMargin: 10
        anchors.rightMargin: 40
        anchors.bottomMargin: 40
        onClicked: {
            med_controller.add_patient(nameFieldWidget.inputText, ageFieldWidget.inputText, sexFieldWidget.currentText,
                                       cholesterolLevelFieldWidget.currentText, bloodPressureFieldWidget.currentText,
                                       difficultyBreathingCheckBoxWidget.checked, fatigueCheckBoxWidget.checked,
                                       coughCheckBoxWidget.checked, feverCheckBoxWidget.checked)
            addPatientDialog.close()
        }
    }

    Text {
        id: patientTitle
        color: "#ffffff"
        text: qsTr("Patient")
        anchors.left: parent.left
        anchors.top: mainTitle.bottom
        anchors.leftMargin: 40
        anchors.topMargin: 24
        font.pixelSize: 18
    }

    Rectangle {
        id: rectangle
        height: 2
        color: "#62667A"
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
        necessarily: true
        inputText: ""
        placeholderText: "Patient Name"
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
        inputText: "0"
        necessarily: true
        fieldName: "Age"
        placeholderText: "Age"

        validator: IntValidator {
            top: 150
            bottom: 0
        }
        inputHints: Qt.ImhDigitsOnly
    }

    ComboFieldWidget {
        id: sexFieldWidget
        width: 230
        height: 64
        anchors.left: ageFieldWidget.right
        anchors.top: rectangle.bottom
        anchors.leftMargin: 6
        anchors.topMargin: 6
        necessarily: true
        current: -1
        fieldTitle: "Sex"
        comboModel: ["Male", "Female"]
    }

    Text {
        id: symptomsTitle
        color: "#ffffff"
        text: qsTr("Symptoms")
        anchors.left: parent.left
        anchors.top: mainTitle.bottom
        anchors.leftMargin: 40
        anchors.topMargin: 164
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
        }

        CheckBoxWidget {
            id: coughCheckBoxWidget
            text: "Cough"
        }

        CheckBoxWidget {
            id: fatigueCheckBoxWidget
            text: "Fatigue"
        }

        CheckBoxWidget {
            id: difficultyBreathingCheckBoxWidget
            text: "Difficulty Breathing"
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
        comboModel: ["Normal", "High"]
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
        comboModel: ["Normal", "High"]
    }

    Text {
        id: text1
        color: "#64687E"
        text: qsTr("(At least one symptom is required)")
        anchors.verticalCenter: symptomsTitle.verticalCenter
        anchors.left: symptomsTitle.right
        anchors.leftMargin: 6
        font.pixelSize: 18
    }
}
