package com.example.crosswordandroidapp

import android.content.Context
import android.content.res.AssetManager
import android.graphics.Paint.Align
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.gestures.snapping.SnapPosition
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material3.Button
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.material3.contentColorFor
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.crosswordandroidapp.ui.theme.CrosswordAndroidAppTheme
import java.util.HashMap
import androidx.navigation.NavController
import androidx.navigation.NavType
import androidx.navigation.compose.*
import androidx.navigation.navArgument

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            CrosswordAndroidAppTheme {
                val navController = rememberNavController()
                NavHost(navController = navController, startDestination = "startScreen"){
                    composable("startScreen") { StartScreen(navController) }
                    composable("loadScreen") { LoadScreen(navController) }
                    composable(
                        route = "crosswordScreen/{fileName}",
                        arguments = listOf(navArgument("fileName") {type = NavType.StringType})
                    ){backStackEntry ->
                        val context = LocalContext.current
                        val fileName = backStackEntry.arguments?.getString("fileName") ?: ""

                        CrosswordScreen(
                            navController = navController,
                            fileName = fileName,
                            context = context
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun StartScreen(navController: NavController) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(64.dp),
        verticalArrangement = Arrangement.SpaceBetween,
        horizontalAlignment = Alignment.CenterHorizontally
    ){
        Text(
            text = "Crossword Game!",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.align(Alignment.CenterHorizontally)
        )

        Column (
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .fillMaxHeight()
                .weight(1f)
        ){
            Button(onClick = {navController.navigate("loadScreen")}, modifier = Modifier.padding(8.dp)) {
                Text("Load")
            }
            Button(onClick = {/*TODO*/}, modifier = Modifier.padding(8.dp)) {
                Text("Scan")
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LoadScreen(navController: NavController){
    val context = LocalContext.current
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(64.dp),
        verticalArrangement = Arrangement.SpaceBetween,
        horizontalAlignment = Alignment.CenterHorizontally
    ){
        Text(
            text = "Crossword Game!",
            style = MaterialTheme.typography.headlineMedium,
            modifier = Modifier.align(Alignment.CenterHorizontally)
        )

        val assetManager = context.assets
        val loadOptions = assetManager.list("")?.toList()?.filter { it.endsWith(".txt") } ?: emptyList()
        var expanded by remember { mutableStateOf(false) }
        var selectedOptionText by remember { mutableStateOf(loadOptions[0])}
        ExposedDropdownMenuBox(
            expanded = expanded,
            onExpandedChange = {
                expanded = !expanded
            }
        ) {
            TextField(
                modifier = Modifier.menuAnchor(),
                readOnly = true,
                value = selectedOptionText,
                onValueChange = { },
                label = { Text("Current Files") },
                trailingIcon = {
                    ExposedDropdownMenuDefaults.TrailingIcon(
                        expanded = expanded
                    )
                },
                colors = ExposedDropdownMenuDefaults.textFieldColors()

            )
            ExposedDropdownMenu(
                expanded = expanded,
                onDismissRequest = {
                    expanded = false
                }
            ) {
                loadOptions.forEach { selectionOption ->
                    DropdownMenuItem(
                        text = {Text(text = selectionOption)},
                        onClick = {
                            selectedOptionText = selectionOption
                            expanded = false
                        }
                    )
                }
            }
        }

        Row (
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier
                .fillMaxHeight()
                .weight(1f)
        ){
            Button(onClick = {navController.navigate("startScreen")}, modifier = Modifier.padding(8.dp)) {
                Text("Back")
            }
            Button(onClick = {navController.navigate("crosswordScreen/$selectedOptionText")}, modifier = Modifier.padding(8.dp)) {
                Text("Begin")
            }
        }
    }
}

@Composable
fun CrosswordScreen(navController: NavController, fileName: String, context: Context){

    val crossword = remember(fileName) {parseCrosswordFile(context,fileName)}
    //TODO process object into image, worry about intractability later
    Column(
        modifier = Modifier.fillMaxSize().padding(64.dp)
    ) {
        Text("Puzzle: ${fileName.split(".")[0]}")
        Text("Row = ${crossword.row} Col = ${crossword.col}")
        Spacer(modifier = Modifier.height(16.dp))

        //Generate square as text boxes?

        Text("Grid data stored:\n ${crossword.printGrid()}")
        Text("Across Clues: ${crossword.getCluesAcross()}")
        Text("Down Clues: ${crossword.getCluesAcross()}")

        Spacer(modifier = Modifier.weight(1f))
        Button(onClick = {navController.navigate("loadScreen")}) { Text("Quit") }
    }
}

fun parseCrosswordFile(context: Context ,fileName: String): Crossword {
    val inputStream = context.assets.open(fileName)
    val fileBuffer = inputStream.bufferedReader()
    //Process Crossword grid dimension (line 1) should be Col then Row
    var currLineString:String = fileBuffer.readLine()
    val parseStr: List<String> = currLineString.split(" ")
    if (parseStr.size != 2){
        println("Invalid matrix dimension $parseStr")
        return Crossword(0,0)
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
        return Crossword(0,0)
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
        return Crossword(0,0)
    }
    return crossword
}

fun parseClueString(inputString: String, hashMapToPop: HashMap<Int,String>){
    val processedString: List<String> = inputString.split(":", limit = 2)
    hashMapToPop[processedString[0].toInt()] = processedString[1]
}
