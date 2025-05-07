import 'camera_screen.dart';
import 'load_crossword_screen.dart';
import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  static const routeName = '/';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crossword Game'),
      ),
      body: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
        const Text('Temp Home Page'),
        TextButton(onPressed: () {
          Navigator.push(context, MaterialPageRoute(builder: (context) => LoadScreen()));
        }, child: const Text("Load")),
        TextButton(onPressed: () {
          Navigator.push(context, MaterialPageRoute(builder: (context) => CameraScreen()));
        }, child: const Text("Capture Crossword"))
        ],
      ),
    );
  }
}
