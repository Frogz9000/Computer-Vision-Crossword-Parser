import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'home_screen.dart';
import 'package:flutter_doc_scanner/flutter_doc_scanner.dart';
//https://pub.dev/packages/flutter_doc_scanner
//https://pub.dev/documentation/path_provider/latest/path_provider/getApplicationDocumentsDirectory.html

class CameraScreen extends StatefulWidget {
  CameraScreen({Key? key}) : super(key: key);
  static const routeName = '/camera';

  @override
  State<CameraScreen> createState() => _CammeraScreenState();
}

class _CammeraScreenState extends State<CameraScreen> {
  dynamic _scannedDocuments;
  
  Future<void> scanDocumentAsPdf() async {
    dynamic scannedDocuments;
    try {
      scannedDocuments =
          await FlutterDocScanner().getScannedDocumentAsPdf(page: 4) ??
              'Unknown platform documents';
    } on PlatformException {
      scannedDocuments = 'Failed to get scanned documents.';
    }
    print(scannedDocuments.toString());
    if (!mounted) return;
    setState(() {
      _scannedDocuments = scannedDocuments;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Document Scanner Example',
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Document Scanner example'),
        ),
        body: Center(
          child: SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _scannedDocuments != null
                    ? Text(_scannedDocuments.toString())
                    : const Text("No Documents Scanned"),
              ],
            ),
          ),
        ),
        floatingActionButton: Padding(
          padding: const EdgeInsets.only(bottom: 16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8.0),
                child: ElevatedButton(
                  onPressed: () {
                    scanDocumentAsPdf();
                  },
                  child: const Text("Scan Documents As PDF"),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 8.0),
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.push(context, MaterialPageRoute(builder: (context) => HomeScreen()));
                  },
                  child: const Text("Quit"),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
