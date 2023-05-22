from havoc.service import HavocService
from havoc.agent import *

class CommandShell(Command):
    CommandId = 18
    Name = "shell"
    Description = "executes commands using cmd.exe"
    Help = ""
    NeedAdmin = False
    Params = [
        CommandParam(
            name="commands",
            is_file_path=False,
            is_optional=False
        )
    ]
    Mitr = []

    def job_generate(self, arguments: dict) -> bytes:
        print("[*] job generate")
        packer = Packer()

        AesKey = base64.b64decode(arguments["__meta_AesKey"])
        AesIV = base64.b64decode(arguments["__meta_AesIV"])

        commands = "/C " + arguments["commands"]
        packer.add_data(commands)

        task_id = int(arguments["TaskID"], 16)
        job = TaskJob(
            command=self.CommandId,
            task_id=task_id,
            data=packer.buffer.decode('utf-8'),
            aes_key=AesKey,
            aes_iv=AesIV
        )

        return job.generate()[4:]


class CommandWmiExec(Command):
    CommandId = 19
    Name = "wmi-execute"
    Description = "executes wmi commands"
    Help = ""
    NeedAdmin = False
    Params = [
        CommandParam(
            name="commands",
            is_file_path=False,
            is_optional=False
        )
    ]
    Mitr = []

    def job_generate(self, arguments: dict) -> bytes:
        print("[*] job generate")
        packer = Packer()

        AesKey = base64.b64decode(arguments["__meta_AesKey"])
        AesIV = base64.b64decode(arguments["__meta_AesIV"])

        packer.add_data(arguments["commands"])

        task_id = int(arguments["TaskID"], 16)
        job = TaskJob(
            command=self.CommandId,
            task_id=task_id,
            data=packer.buffer.decode('utf-8'),
            aes_key=AesKey,
            aes_iv=AesIV
        )

        return job.generate()[4:]

    def response( self, resp: dict ) -> dict:

        decoded = base64.b64decode(resp["Response"])
        parser = Parser(decoded, len(decoded))
        output = parser.parse_bytes()

        return {
            "Type": "Good",
            "Message": f"Received WMI Output [{len(output)} bytes]",
            "Output": output.decode('utf-8')
        }


class Azazel(AgentType):
    Name = "Azazel"
    Author = "@C5pider"
    Version = "0.1"
    Description = f"""Test Description version: {Version}"""
    MagicValue = 0xdeaddead

    Formats = [
        {
            "Name": "Windows Executable",
            "Extension": "exe",
        },
        {
            "Name": "Windows Dll",
            "Extension": "dll",
        },
        {
            "Name": "Windows Service Exe",
            "Extension": "exe",
        },
        {
            "Name": "Windows Reflective Dll",
            "Extension": "dll",
        },
        {
            "Name": "Windows Raw Binary",
            "Extension": "bin",
        },
    ]

    BuildingConfig = {

        "TestText": "DefaultValue",

        "TestList": [
            "list 1",
            "list 2",
            "list 3",
        ],

        "TestBool": True,

        "TestObject": {
            "TestText": "DefaultValue",
            "TestList": [
                "list 1",
                "list 2",
                "list 3",
            ],
            "TestBool": True,
        }
    }

    SupportedOS = [
        SupportedOS.Windows
    ]

    Commands = [
        CommandShell(),
        CommandWmiExec(),
    ]

    def generate( self, config: dict ) -> None:

        self.builder_send_message( config[ 'ClientID' ], "Info", f"hello from service builder" )
        self.builder_send_message( config[ 'ClientID' ], "Info", f"Options Config: {config['Options']}" )
        self.builder_send_message( config[ 'ClientID' ], "Info", f"Agent Config: {config['Config']}" )

        self.builder_send_payload( config[ 'ClientID' ], self.Name + ".bin", "test bytes".encode('utf-8') )

    def command_not_found(self, response: dict) -> dict:
        if response["CommandID"] == 90:  # CALLBACK_OUTPUT

            decoded = base64.b64decode(response["Response"])
            parser = Parser(decoded, len(decoded))
            output = parser.parse_bytes()

            return {
                "Type": "Good",
                "Message": f"Received Output [{len(output)} bytes]",
                "Output": output.decode('utf-8')
            }

        return {
            "Type": "Error",
            "Message": f"Command not found: [CommandID: {response['CommandID']}]",
        }


def main():
    Havoc_Azazel = Azazel()
    Havoc_Service = HavocService(
        endpoint="wss://192.168.0.148:40056/test",
        password="password1234"
    )

    Havoc_Service.register_agent(Havoc_Azazel)

    return


if __name__ == '__main__':
    main()
