import QtQuick 2.0
import QtQuick.Window 2.2
import QtQuick.Controls 2.0

Window {
    id: idRoot
    width: 1200
    height: 720
    visible: true

    property bool bLoadReports: false
    Background {
        width: 1200
        height: 700

    }

   MenuCustom {
       bLoadReport: idRoot.bLoadReports
       onBLoadReportChanged: {
           console.log ("Load repppppppppppppppppppppport")
           rep.z = 3

       }
   }

   
   Reports {
       id: rep
       visible: bLoadReports
   }
  



}
