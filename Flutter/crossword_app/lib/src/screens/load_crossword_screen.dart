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
      body: const Center(
        child: Text('Temp Load Page'),
      ),
    );
  }
}
