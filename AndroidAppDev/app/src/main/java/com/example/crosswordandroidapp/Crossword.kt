package com.example.crosswordandroidapp

import androidx.core.text.isDigitsOnly


class Crossword(val row: Int, val col: Int) {
    data class CrosswordCell(val cellType: String, val cellContent: Char = ' ')
    private var gridData : ArrayList<CrosswordCell> = ArrayList()

    
    
    //Pass in the format string(line 2 of the txt) to populate the blank crossword
    //Returns 0 if success, other for failure
    //Modifies: gridData
    fun populateGridData(fileString: String): Int {
        val subStrings = fileString.split(",")
            for (i in 0..<(row * col)){
                val currentVal = subStrings[i]
                val currentCell : CrosswordCell;
                if (currentVal == "X"){//Black Square
                    currentCell = CrosswordCell("Black")
                }
                else if (currentVal == "O") {//Empty square for entering
                    currentCell = CrosswordCell("Empty")
                }
                else if (currentVal.isDigitsOnly()){//clue tile
                    currentCell = CrosswordCell(currentVal)
                }
                else{
                    println("Invalid Grid Format String Provided")
                    return 1;
                }
                gridData[i] = currentCell;
            }
        return 0;
    }
    
    fun printGridData(){
        for (i in 0..<gridData.size){
            print(gridData[i].cellType)
            if (i%(row-1) == 0){
                println()
            }
        }
    }
}