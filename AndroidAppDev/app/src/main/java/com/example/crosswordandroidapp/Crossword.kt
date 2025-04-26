package com.example.crosswordandroidapp

import android.util.Log
import androidx.core.text.isDigitsOnly
import java.util.Dictionary
import java.util.HashMap
import kotlin.text.StringBuilder


class Crossword(val row: Int, val col: Int) {
    data class CrosswordCell(val cellType: String, val cellContent: Char = ' ')
    private var gridData : ArrayList<CrosswordCell> = ArrayList()
    private var cluesAcross = hashMapOf<Int, String>()
    private var cluesDown = hashMapOf<Int, String>()

    fun setCluesAcross(hashMap: HashMap<Int,String>){
        cluesAcross = hashMap
    }
    fun getCluesAcross(): HashMap<Int,String>{
        return cluesAcross
    }
    fun setCluesDown(hashMap: HashMap<Int,String>){
        cluesDown = hashMap
    }
    fun getCluesDown(): HashMap<Int,String>{
        return cluesDown
    }
    //Pass in the format string(line 2 of the txt) to populate the blank crossword
    //Returns 0 if success, other for failure
    //Modifies: gridData
    fun populateGridData(fileString: String): Int {
        val subStrings = fileString.split(",")
            for (element in subStrings){
                val currentCell : CrosswordCell
                if (element == "X") {//Black Square
                    currentCell = CrosswordCell("Black")
                } else if (element == "O") {//Empty square for entering
                    currentCell = CrosswordCell("Empty")
                } else if (element.isDigitsOnly()) {//clue tile
                    currentCell = CrosswordCell(element)
                } else {
                    println("Invalid Grid Format String Provided")
                    return 1
                }
                gridData.add(currentCell)
            }
        return 0
    }

    fun printGrid(): String {
        val buff = StringBuilder()
        for (i in 0 until row) {
            for (j in 0 until col) {
                val index = i * row + j
                buff.append(gridData[index].cellType).append(" ")
            }
            buff.append("\n")
        }
        return buff.toString()
    }
}