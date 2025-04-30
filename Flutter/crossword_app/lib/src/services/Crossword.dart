import 'package:tuple/tuple.dart';
import 'dart:async';
import 'dart:io';

class Crossword {
  final String fileName;
  late final Tuple2 dimensions;
  late final List<String> layoutData;
  late final Map<int,String> acrossClues;
  late final Map<int,String> downClues;
  //private constructor
  Crossword._(this.fileName);
  //method to generate class with file Parsing
  static Future<Crossword> fromFile(String filename) async {
    final crossword = Crossword._(filename);
    final file = File(filename);
    final lines = await file.readAsLines();
    var acrossFlag = 0;
    var downFlag = 0;
    Map<int,String> clueBuilder = {};
    for (var lineIndex = 0; lineIndex < lines.length;lineIndex++){
      //parsing done here
      if (lineIndex == 0){//get matrix size from first line
        List<String> dim = lines[lineIndex].split(" ");
        crossword.dimensions = Tuple2(int.parse(dim[0]),int.parse(dim[1]));
        continue;
      }
      if (lineIndex == 1){//get matrix layout data
        crossword.layoutData = lines[lineIndex].split(",");
        continue;
      }
      //Process Across
      if(lines[lineIndex] == "ACROSS"){
        acrossFlag = 1;
        continue;
      }
      if (acrossFlag == 1){
        var current = lines[lineIndex];
        if (current == "END_ACROSS"){
          acrossFlag = 0;
          crossword.acrossClues = clueBuilder;
          clueBuilder = {};
          continue;
        }
        var clue = current.split(":");
        clueBuilder[int.parse(clue[0])] = clue[1].trim();
        continue;
      }
      //Process Down
      if(lines[lineIndex] == "DOWN"){
        downFlag = 1;
        continue;
      }
      if (downFlag == 1){
        var current = lines[lineIndex];
        if (current == "END_DOWN"){
          downFlag = 0;
          crossword.downClues = clueBuilder;
          clueBuilder = {};
          continue;
        }
        var clue = current.split(":");
        clueBuilder[int.parse(clue[0])] = clue[1].trim();
        continue;
      }
    }
    return crossword;
  }
}