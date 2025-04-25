package com.example.crosswordandroidapp

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.crosswordandroidapp.ui.theme.CrosswordAndroidAppTheme
import java.io.BufferedReader
import java.io.File
import java.util.HashMap

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        //parseCrosswordFile(this,"testFileFormat.txt")
        enableEdgeToEdge()
        setContent {
            CrosswordAndroidAppTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    Greeting(
                        name = "Android",
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}



fun parseCrosswordFile(context: Context ,fileName: String): Int {
    val inputStream = context.assets.open(fileName)
    val fileBuffer = inputStream.bufferedReader()
    //Process Crossword grid dimension (line 1) should be Col then Row
    var currLineString:String = fileBuffer.readLine()
    val parseStr: List<String> = currLineString.split(" ")
    if (parseStr.size != 2){
        println("Invalid matrix dimension $parseStr")
        return 1
    }
    val crossword = Crossword(parseStr[1].toInt(), parseStr[0].toInt())

    //Process Grid Template
    currLineString = fileBuffer.readLine()
    crossword.populateGridData(currLineString)

    //Process Across Clues
    currLineString = fileBuffer.readLine()
    if (currLineString == "ACROSS"){
        var acrossHash = hashMapOf<Int,String>()
        while(true){
            currLineString = fileBuffer.readLine()
            if (currLineString == "END_ACROSS"){
                break;
            }
            parseClueString(currLineString,acrossHash)
        }
        crossword.setCluesAcross(acrossHash)
    }else{
        print("Invalid file format: expected across got $currLineString")
        return 1
    }

    //Process Down Clues
    currLineString = fileBuffer.readLine()
    if (currLineString == "DOWN"){
        var downHash = hashMapOf<Int,String>()
        while(true){
            currLineString = fileBuffer.readLine()
            if (currLineString == "END_DOWN"){
                break
            }
            parseClueString(currLineString,downHash)
        }
        crossword.setCluesDown(downHash)
    }else{
        print("Invalid file format: expected across got $currLineString")
        return 1
    }
    return 0
}

fun parseClueString(inputString: String, hashMapToPop: HashMap<Int,String>){
    val processedString: List<String> = inputString.split(":", limit = 2)
    hashMapToPop[processedString[0].toInt()] = processedString[1]
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    CrosswordAndroidAppTheme {
        Greeting("Android")
    }
}