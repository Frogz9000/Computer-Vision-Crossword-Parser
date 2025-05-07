import 'load_crossword_screen.dart';
import 'package:flutter/material.dart';

class PlayScreen extends StatelessWidget {
  const PlayScreen({super.key});

  static const routeName = '/play';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crossword Game'),
      ),
      body: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
        const Text('Temp Play Page'),
        TextButton(onPressed: () {
          Navigator.push(context, MaterialPageRoute(builder: (context) => LoadScreen()));
        }, child: const Text("Quit"))
        ],
      ),
    );
  }
}
