# Understanding AI Agents
## Session labs 
## Revision 4.1 - 09/09/25

**Follow the startup instructions in the README.md file IF NOT ALREADY DONE!**

**NOTE: To copy and paste in the codespace, you may need to use keyboard commands - CTRL-C and CTRL-V. Chrome may work best for this.**

**Lab 1 - Creating a simple agent**

**Purpose: In this lab, we’ll learn about the basics of agents and see how tools are called. We'll also see how Chain of Thought prompting works with LLMs and how we can have ReAct agents reason and act.**

1. In our repository, we have a set of Python programs that we'll be building out to work with concepts in the labs. These are mostly in the *agents* subdirectory. Go to the *TERMINAL* tab in the bottom part of your codespace and change into that directory.
```
cd agents
```

2. For this lab, we have the outline of an agent in a file called *agent1.py* in that directory. You can take a look at the code either by clicking on [**agents/agent1.py**](./agents/agent1.py) or by entering the command below in the codespace's terminal.
   
```
code agent1.py
```

3. If you scroll through this file, you can see it outlines the steps the agent will go through without all the code. When you are done looking at it, close the file by clicking on the "X" in the tab at the top of the file.

4. Now, let's fill in the code. To keep things simple and avoid formatting/typing frustration, we already have the code in another file that we can merge into this one. Run the command below in the terminal.
```
code -d ../extra/lab1-code.txt agent1.py
```

5. Once you have run the command, you'll have a side-by-side view in your editor of the completed code and the agent1.py file.
  You can merge each section of code into the agent1.py file by hovering over the middle bar and clicking on the arrows pointing right. Go through each section, look at the code, and then click to merge the changes in, one at a time.

![Side-by-side merge](./images/aa40.png?raw=true "Side-by-side merge") 

6. When you have finished merging all the sections in, the files should show no differences. Save the changes simply by clicking on the "X" in the tab name.

![Merge complete](./images/aa41.png?raw=true "Merge complete") 

7. Now you can run your agent with the following command:

```
python agent1.py
```

8. The agent will start running and will prompt for a location (or "exit" to finish). At the prompt, you can type in a location like "Paris, France" or "London" or "Raleigh" and hit *Enter*. After that you'll be able to see the Thought -> Action -> Observation loop in practice as each one is listed out. You'll also see the arguments being passed to the tools as they are called. Finally you should see a human-friendly message from the AI summarizing the weather forecast.  (**NOTE: Since this is having to load up the model initially, it will take up to 3 minutes to return the first response.**)

![Agent run](./images/aa42.png?raw=true "Agent run") 

9. You can then input another location and run the agent again or exit. Note that if you get a timeout error, the API may be limiting the number of accesses in a short period of time. You can usually just try again and it will work.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 2 - Exploring MCP**

**Purpose: In this lab, we’ll see how MCP can be used to standardize an agent's interaction with tools.**

1. Still in the *agents* directory, we have partial implementations of an MCP server and an agent that uses a MCP client to connect to tools on the server. So that you can get acquainted with the main parts of each, we'll build them out as we did the agent in the first lab - by viewing differences and merging. Let's start with the server. Run the command below to see the differences.

```
code -d ../extra/lab2-server.txt mcp_server.py
```
</br></br>
![MCP server code](./images/aa43.png?raw=true "MCP server code") 

2. As you look at the differences, note that we are using FastMCP to more easily set up a server, with its @mcp.tool decorators to designate our functions as MCP tools. Also, we run this using the *streamable-http* transport protocol. Review each difference to see what is being done, then use the arrows to merge. When finished, click the "x"" in the tab at the top to close and save the files.

3. Now that we've built out the server code, run it using the command below. You should see some startup messages similar to the ones in the screenshot.

```
python mcp_server.py
```
</br></br>
![MCP server start](./images/aa44.png?raw=true "MCP server start") 

4. Now, let's turn our attention to the agent that will use the MCP server through an MCP client interface. First, since the terminal is tied up with the running server, we need to have a second terminal to use to work with the client. So that we can see the server responses, let's just open another terminal side-by-side with this one. To do that, right-click in the current terminal and select *Split Terminal* from the pop-up context menu.

![Opening a second terminal](./images/aa45.png?raw=true "Opening a second terminal") 

5. In the second terminal, run a diff command so we can build out the new agent.

```
code -d ../extra/lab2-code.txt mcp_agent.py
```

6. Review and merge the changes as before. What we're highlighting in this step are the *System Prompt* that drives the LLM used by the agent, the connection with the MCP client at the /mcp/ endpoint (line 55), and the mpc calls to the tools on the server. When finished, close the tab to save the changes as before.

![Agent using MCP client code](./images/aa75.png?raw=true "Agent using MCP client code") 
   
7. After you've made and saved the changes, you can run the client in the terminal with the command below.

```
python mcp_agent.py
```

8. The agent should start up, and, as in lab 1, prompt you for a location. You'll be able to see similar TAO output. And you'll also be able to see the server INFO messages in the other terminal as the MCP connections and events happen.

![Agent using MCP client running](./images/aa76.png?raw=true "Agent using MCP client running") 

9. When you're done, you can use 'exit' to stop the client and CTRL-C to stop the server. 

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 3 - Leveraging Coding Agents and Memory**

**Purpose: In this lab, we’ll see how agents can drive solutions via creating code and implement simple memory techniques using the smolagents framework.**

1. For this lab, we have a simple application that does currency conversion using prompts of the form "Convert 100 USD to EUR", where *USD* = US dollars and *EUR* = euros.  It will also remember previous values and invocations.


2. As before, we'll use the "view differences and merge" technique to learn about the code we'll be working with. The command to run this time is below:

```
code -d ../extra/curr_conv_agent.txt curr_conv_agent.py
```
</br></br>

![Code for memory agent](./images/aa68.png?raw=true "Code for memory agent") 

3. The code in this application showcases several SmolAgents features and agent techniques including the following. See how many you can identify as your reviewing the code.

- **@tool decorator** turns your Python functions into callable “tools” for the agent.  
- **LiteLLMModel** plugs in your local Ollama llama3.2 as the agent’s reasoning engine.  
- **CodeAgent** runs a ReAct loop: think (LLM), act (call tool), observe, repeat.  
- **Controlled toolset** (`add_base_tools=False`) limits the agent to only your defined tools.  
- **Deterministic output** (`temperature=0.0`) ensures consistent tool selection and results.  
- **Tool chaining** lets the agent fetch live rates, then compute conversions in sequence.  
- **Memory feature** remembers current values and persists them (with history) to an external JSON file.  


4. When you're done merging, close the tab as usual to save your changes. Now, in a terminal, run the agent with the command below:

```
python curr_conv_agent.py
```

5. Enter a basic prompt like the one below.

```
Convert 100 USD to EUR
```

6. The agent will run for a while and not return as the LLM loads and the processing happens. When it is finished with this run, you'll see output like the screenshot below. Notice that since we used the SmolAgents CodeAgent type, you can see the code it created and executed in the black box. **NOTE: This initial run will take several minutes!**

![Running agent](./images/aa69.png?raw=true "Running agent")   

7. Now you can try some partial inputs with missing values to demonstrate the agent remembering arguments that were passed to it before. Here are some to try. Output is shown in the screenshot. (You may see some intermediate steps. You're looking for the one with "Final answer" in it.)

```
Convert 200
Convert 400 to JPY
```

![Running with partial inputs](./images/aa70.png?raw=true "Running agent")  
![Running with partial inputs](./images/aa71.png?raw=true "Running agent")   


8. To see the stored history information on disk, type "exit" to exit the tool. Then in the terminal type the command below to see the contents of the file.

```
cat currency_memory.json
```

![Running with partial inputs](./images/aa72.png?raw=true "Running agent") 

9. Finally, you can start the agent again and enter "history" at the prompt to see the persisted history from before. Then you can try a query and it should pick up as before. In the example, we used the query below:

```
convert 300
```

![Running with partial inputs](./images/aa73.png?raw=true "Running agent")   


10.  Just type "exit" when ready to quit the tool.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

    
**Lab 4 - Using RAG with Agents**

**Purpose: In this lab, we’ll explore how agents can leverage external data stores via RAG**

1. For this lab, we have an application that does the following:

- Reads, processes, and stores information about company offices from a PDF file
- Lets you input a starting location
- Lets you prompt about a destination location such as an office name
- Maps the destination back to data taken from the PDF if it can
- Uses the destination from the PDF data or from the prompt to  
  - Find and provide 3 interesting facts about the destination
  - Calculate distance from the starting location to the destination
- Stores information about starting location in an external file
- Repeats until user enters *exit*

2. The PDF file we're using to illustrate RAG here is a fictional list of offices and related info for a company. You can see it in the repo at  [**data/offices.pdf**](./data/offices.pdf) 

![Data pdf](./images/aa66.png?raw=true "Data pdf") 


3. As before, we'll use the "view differences and merge" technique to learn about the code we'll be working with. The command to run this time is below. The code differences mainly hightlight the changes for RAG use in the agent, including working with vector database and snippets returned from searching it.
   
```
code -d ../extra/rag_agent.txt rag_agent.py
```
</br></br>

![Code for rag agent](./images/aa65.png?raw=true "Code for rag agent") 


4. When you're done merging, close the tab as usual to save your changes. Now, in a terminal, run the agent with the command below:

```
python rag_agent.py
```

5. You'll see the agent loading up the embedding pieces it needs to store the document in the vector database. After that you can choose to override the default starting location, or leave it on the default. You'll see a *User:* prompt when it is ready for input from you. The agent is geared around you entering a prompt about an office. Try a prompt like one of the ones below about office "names" that are only in the PDF.

```
Tell me about HQ
Tell me about the Southern office
```

6. What you should see after that are some messages that show internal processing, such as the retrieved items from the RAG datastore.  Then the agent will run through the necessary steps like geocoding locations, calculating distance, using the LLM to get interesting facts about the city etc. At the end it will print out facts about the office location, and the city the office is in, as well as the distance to the office.
 
![Running the RAG agent](./images/aa67.png?raw=true "Running the RAG agent") 

7. The stored information about startup location is in a file named *user_starting_location.json* in the same directory if you want to view that.

8. After the initial run, you can try prompts about other offices or cities mentioned in the PDF. Type *exit* when done.

<p align="center">
**[END OF LAB]**
</p>
</br></br>

**Lab 5 - Working with multiple agents**

**Purpose: In this lab, we’ll see how to add an agent to a workflow using CrewAI.**

1. As we've done before, we'll build out the agent code with the diff/merge facility. Run the command below.
```
code -d ../extra/lab5-code.txt agent5.py
```

![Diffs](./images/aa23.png?raw=true "Diffs") 

2. In the *agent5.py* template, we have the imports and llm setup at the top filled in, along with a simulated function to book a flight. Scroll to the bottom. At the bottom is the input and code to kick off the "*crew*". So, we need to fill in the different tasks and setup the crew.

3. Scroll back to the top, review each change and then merge each one in. Notice the occurrences of "*booking_agent*". This is all being done with a single agent in the crew currently. When done, the files should show no differences. Click on the "X" in the tab at the top to save your changes to *agent5.py*.

![Merge complete](./images/aa24.png?raw=true "Merge complete") 

4. Now you can run the agent and see the larger workflow being handled. There will be quite a bit of output so this may take a while to run. **NOTE: Even though the agent may prompt for human input to select a flight, none is needed. We're not adding that in and using fake info to keep things simple and quick.**

```
python agent5.py
```

![Execution](./images/aa31.png?raw=true "Execution") 

5. Now, that we know how the code works and that it works, let's consider the overall approach. Since there are multiple functions going on here (getting info, finding flights, booking flights) it doesn't necessarily make sense to have just one agent doing all those things. Let's add two other agents - a *travel agent* to help with finding flights, and a customer_service_agent to help with user interactions. To start, open the code for editing.

```
code agent5.py
```


6. Now, replace the single *booking agent* definition with these definitions for the 3 agents (making sure to get the indenting correct):


**Directions:** Copy the block of replacement text in gray below and paste over the single agent definition in the code. Reminder - you may need to use keyboard shortcuts to copy and paste. The screenshots are only to show you before and after - they are not what you copy.

```
# Defines the AI agents

booking_agent = Agent(
    role="Airline Booking Assistant",
    goal="Help users book flights efficiently.",
    backstory="You are an expert airline booking assistant, providing the best booking options with clear information.",
    verbose=True,
    llm=ollama_llm,
)

# New agent for travel planning tasks
travel_agent = Agent(
    role="Travel Assistant",
    goal="Assist in planning and organizing travel details.",
    backstory="You are skilled at planning and organizing travel itineraries efficiently.",
    verbose=True,
    llm=ollama_llm,
)

# New agent for customer service tasks
customer_service_agent = Agent(
    role="Customer Service Representative",
    goal="Provide excellent customer service by handling user requests and presenting options.",
    backstory="You are skilled at providing customer support and ensuring user satisfaction.",
    verbose=True,
    llm=ollama_llm,
)
```
![Text to replace](./images/aa26.png?raw=true "Text to replace") 

![Replaced text](./images/aa27.png?raw=true "Replaced text")

7. Next, we'll change each *task definition* to reflect which agent should own it. The places to make the change are in the task definitions in the lines that start with "*agent=*". Just edit each one as needed per the mapping in the table below. The screenshot below the mappings shows what the changed code should look like.

| **Task** | *Agent* | 
| :--------- | :-------- | 
| **extract_travel_info_task** |  *customer_service_agent*  |        
| **find_flights_task** |  *travel_agent*  |  
| **present_flights_task** |  *customer_service_agent*  |  
| **book_flight_task** | *booking_agent* (ok as-is) |  
         
![Replaced text](./images/aa28.png?raw=true "Replaced text")

8. Finally, we need to add the new agents to our crew. Edit the "*agents=[*" line in the block under the comment "*# Create the crew*". In that line, add *customer_service_agent* and *travel_agent*. The full line is below. The screenshot shows the changes made.

```
agents=[booking_agent, customer_service_agent, travel_agent],
```

![Replaced text](./images/aa29.png?raw=true "Replaced text")

9. Now you can save your changes and then run the program again.

```
python agent5.py
```

10. This time when the code runs, you should see the different agents being used in the processing.

![Run with new agents](./images/aa30.png?raw=true "Run with new agents")

<p align="center">
**[END OF LAB]**
</p>
</br></br>
 

<p align="center">
**THANKS!**
</p>
