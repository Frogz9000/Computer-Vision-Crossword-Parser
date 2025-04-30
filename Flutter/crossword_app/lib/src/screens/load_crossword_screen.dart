import 'package:crossword_app/src/screens/play_crossword_screen.dart';
import 'package:flutter/material.dart';

class LoadScreen extends StatelessWidget {
  const LoadScreen({super.key});

  static const routeName = '/load';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crossword Game'),
      ),
      body: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
        const Text('Temp Load Page'),
        TextButton(onPressed: () {
          Navigator.push(context, MaterialPageRoute(builder: (context) => PlayScreen()));
        }, child: const Text("Play"))
        ],
      ),
    );
  }
}
