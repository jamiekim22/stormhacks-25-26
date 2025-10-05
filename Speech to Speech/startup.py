import os
import json
import subprocess
import argparse
from dotenv import load_dotenv

def create_config_from_env():
    """
    Loads variables from .env and creates a Python dictionary for the JSON config.
    """
    # Load environment variables from .env file into the environment
    load_dotenv()
    
    print("Loaded variables from .env file.")

    # Create a dictionary with the required configuration
    # os.getenv() reads from the loaded environment
    eleven = os.getenv("ELEVENLABS_API_KEY")
    config_data = {
        "account": os.getenv("TWILIO_ACCOUNT_SID"),
        "token": os.getenv("TWILIO_AUTH_TOKEN"),
        "number": os.getenv("TWILIO_AGENT_NUMBER"),
        "domain": os.getenv("TWILIO_DOMAIN"),
        "openai": os.getenv("OPEN_API_KEY"),
        "device": os.getenv("DEVICE"),
    }
    
    return [eleven, config_data]

def run_target_script():
    try:
        # Using a list for the command is more secure and robust
        command = ["python.exe", 's2s_pipeline.py', 'config.json']
        
        # subprocess.run executes the command. check=True will raise an error
        # if the script returns a non-zero exit code (i.e., if it fails).
        subprocess.run(command, check=True)
        
    except FileNotFoundError:
        print(f"Error: The script s2s_pipeline.py was not found.")
    except subprocess.CalledProcessError as e:
        print(f"Error: The script s2s_pipeline.py failed with exit code {e.returncode}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    # 1. Set up argument parser to accept the target script's name
    parser = argparse.ArgumentParser(
        description="Generates a config.json from .env and runs a target Python script."
    )
    parser.add_argument(
        "target_script", 
        help="The path to the Python script to run after creating the config."
    )
    args = parser.parse_args()

    config_file_path = "config.json"
    
    try:
        # 2. Generate config data from the .env file
        eleven, config = create_config_from_env()


        # exporting elevenlab key, need to do this everytimt idk why
        command = ["export", "ELEVENLABS_API_KEY='"+eleven+"'"]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: The script to generate elevenLab token failed with exit code {e.returncode}.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


        # 3. Read the base data and write to a new config.json
        data={}
        with open('./config_gemini_custom.json', 'r') as f:
            data = json.load(f)
        
        data['device'] = config['device']
        data['open_api_api_key'] = config['openai']
        data['twilio_account_sid'] = config['account']
        data['twilio_auth_token'] = config['token']
        data['twilio_phone_number'] = config['number']
        data['twilio_domain'] = config['domain']
        data['twilio_user_number'] = '+16047832553'

        with open(config_file_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Successfully created '{config_file_path}'.")

        # 4. Run the python command for the target script
        run_target_script()

    finally:
    #     # 5. Clean up: always remove the temporary config file
    #     if os.path.exists(config_file_path):
    #         os.remove(config_file_path)
    #         print(f"\nCleanup complete. Removed '{config_file_path}'.")

if __name__ == "__main__":
    main()
