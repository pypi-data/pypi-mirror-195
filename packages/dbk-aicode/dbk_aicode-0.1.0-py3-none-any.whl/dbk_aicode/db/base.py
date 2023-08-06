import os
from typing import List
from supabase import create_client, Client

from dotenv import load_dotenv
load_dotenv()
url: str = os.environ.get('SUPABASE_URL')
key: str = os.environ.get('SUPABASE_KEY')

supabase: Client = create_client(url, key)

def push_logs(run_id: str, project_id: str, logs: List[str]) -> None:
  if len(logs) > 0:
    supabase.table('deployments').upsert(
      json={
        'id': run_id,
        'logs': logs,
        'project_id': project_id,
      },
    ).execute()