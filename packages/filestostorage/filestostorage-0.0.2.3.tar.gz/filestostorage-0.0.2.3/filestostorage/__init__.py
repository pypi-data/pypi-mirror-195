from rich.prompt import Prompt
from rich.console import Console
from rich.progress import Progress, BarColumn, DownloadColumn, TextColumn, TransferSpeedColumn, TimeRemainingColumn
import gridfs
import certifi
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

console = Console()

def mongo_conn():
    global url 
    url = Prompt.ask("Enter your MongoUrl:")
    try:
        conn = MongoClient(url, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
        conn.admin.command('ismaster')
        console.print("Connected to Database", style="bold green")
        return conn.grid_file
    except ConnectionFailure:
        console.print("Wrong URL or check with your connection", style="bold red")
        
def upload_file(file_url, file_name, db1):
    file_location = file_url
    with Progress(TextColumn("[bold blue]{task.fields[filename]}", justify="right"), 
                  BarColumn(), 
                  TextColumn("[bold blue]{task.fields[info]}", justify="center"),
                  TextColumn("[bold blue]{task.fields[transferspeed]}", justify="right"),
                  TextColumn("[bold blue]{task.fields[timeremaining]}", justify="right")) as progress:
        task_id = progress.add_task("[green]Uploading...", filename=file_name, info="", transferspeed="0 B/s", timeremaining="Calculating...")
        file_data = open(file_location, "rb")
        fs = gridfs.GridFS(db1)
        data = file_data.read()
        fs.put(data, filename=file_name)
        progress.update(task_id, completed=100, info="Completed", transferspeed="", timeremaining="")
    console.print("Upload success", style="bold green")

def download_file(download_path, file_name, db1):
    fs1 = gridfs.GridFS(db1)
    data = db1.fs.files.find_one({'filename': file_name})
    my_id = data['_id']
    outputdata = fs1.get(my_id).read()
    download_location = download_path
    with Progress(TextColumn("[bold blue]{task.fields[filename]}", justify="right"), 
                  BarColumn(), 
                  TextColumn("[bold blue]{task.fields[info]}", justify="center"),
                  TransferSpeedColumn(),
                  TimeRemainingColumn()) as progress:
        task_id = progress.add_task("[green]Downloading...", filename=file_name, info="", total=len(outputdata))
        output = open(download_location, "wb")
        output_size = len(outputdata)
        chunk_size = 1024
        num_bars = output_size // chunk_size
        for i in range(num_bars):
            output.write(outputdata[i*chunk_size:(i+1)*chunk_size])
            progress.update(task_id, advance=chunk_size)
        output.write(outputdata[num_bars*chunk_size:])
        progress.update(task_id, completed=output_size, info="Completed", transferspeed="", timeremaining="")
    output.close()
    console.print("Download success", style="bold green")

db = mongo_conn()

db = mongo_conn()


upload_file("/Users/sahilapte/Desktop/mcbc/scam.pdf","hsa",db)
download_file("/Users/sahilapte/Downloads/scams.pdf","hsa",db)