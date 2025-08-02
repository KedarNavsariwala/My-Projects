from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Dict, List
import json
import os

class LLMProcessor:
    def __init__(self, model_name: str = "numind/NuExtract-tiny"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # Load model in 4-bit precision using bitsandbytes
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16,
            quantization_config={
                "load_in_4bit": True,
                "bnb_4bit_compute_dtype": torch.float16,
                "bnb_4bit_use_double_quant": True,
                "bnb_4bit_quant_type": "nf4"
            }
        )
        self.model.eval()

    def process_text(self, text: str, max_length: int = 2000) -> str:
        """Process text through the LLM model to extract grant information."""
        prompt = f"""Extract the following information from the grant document into a structured format:
        - Grant ID
        - Funding Program
        - Funding Agency
        - Field of Interest
        - Submission Date (YYYY-MM-DD format)
        - Requested Amount (numerical value)
        - Duration in Years (numerical value)
        - Institution
        - Title
        - Abstract
        - Specific Aims
        - Methodology
        - Innovation
        - Broader Impacts

        Format the response as a JSON object following this exact structure.
        If any field is not found in the text, use null.

        Here's the grant text to analyze:
        {text}"""
        
        messages = [
            {"role": "user", "content": prompt},
        ]
        
        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        return self.tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)

    def update_json_dataset(self, output_dir: str, grant_id: str, content: Dict) -> None:
        """Update the JSON dataset with new content and validate against schema."""
        json_path = os.path.join(output_dir, 'grants_dataset.json')
        
        # Schema for validation
        schema = {
            "type": "object",
            "properties": {
                "grant_id": {"type": "string"},
                "funding_program": {"type": "string"},
                "funding_agency": {"type": "string"},
                "field_of_interest": {"type": "string"},
                "submission_date": {"type": "string", "format": "date"},
                "requested_amount": {"type": "number"},
                "duration_years": {"type": "integer"},
                "institution": {"type": "string"},
                "title": {"type": "string"},
                "abstract": {"type": "string"},
                "specific_aims": {"type": "string"},
                "methodology": {"type": "string"},
                "innovation": {"type": "string"},
                "broader_impacts": {"type": "string"}
            },
            "required": [
                "grant_id", "funding_program", "funding_agency", 
                "field_of_interest", "submission_date", "requested_amount",
                "duration_years", "institution", "title", "abstract",
                "specific_aims", "methodology", "innovation", "broader_impacts"
            ]
        }
        
        # Load existing data if file exists
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                dataset = json.load(f)
        else:
            dataset = {}
        
        try:
            # Parse the LLM output if it's a string
            if isinstance(content, str):
                content = json.loads(content)
            
            # Ensure all required fields are present
            for field in schema["required"]:
                if field not in content:
                    content[field] = None
            
            # Update dataset
            dataset[grant_id] = content
            
            # Save updated dataset
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, indent=2)
                
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for grant {grant_id}: {e}")
        except Exception as e:
            print(f"Error updating dataset for grant {grant_id}: {e}")
