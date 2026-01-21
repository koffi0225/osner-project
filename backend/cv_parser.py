import PyPDF2
import docx
import os
import json
from typing import Dict, Any
from emergentintegrations.llm.chat import LlmChat, UserMessage
from dotenv import load_dotenv

load_dotenv()

class CVParser:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment")
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error extracting DOCX: {str(e)}")
    
    async def parse_cv(self, cv_text: str) -> Dict[str, Any]:
        """Parse CV text using GPT-5.2 to extract structured information"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id=f"cv_parsing_{id(cv_text)}",
            system_message="""Tu es un expert en analyse de CV. Extrais les informations suivantes du CV de manière structurée:
            - Compétences techniques
            - Expérience professionnelle (postes, entreprises, durées)
            - Formation/Éducation
            - Langues
            - Certifications
            
            Réponds UNIQUEMENT en format JSON valide."""
        ).with_model("openai", "gpt-5.2")
        
        user_message = UserMessage(
            text=f"""Analyse ce CV et extrais les informations en JSON :
            
            {cv_text}
            
            Format attendu :
            {{
                "competences": ["compétence1", "compétence2"],
                "experience": [
                    {{
                        "poste": "titre",
                        "entreprise": "nom",
                        "duree": "période",
                        "description": "résumé"
                    }}
                ],
                "formation": [
                    {{
                        "diplome": "titre",
                        "etablissement": "nom",
                        "annee": "année"
                    }}
                ],
                "langues": ["langue: niveau"],
                "certifications": ["certification1"]
            }}"""
        )
        
        response = await chat.send_message(user_message)
        
        # Parse JSON response
        import json
        try:
            # Remove markdown code blocks if present
            response_text = response.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            parsed_data = json.loads(response_text)
            return parsed_data
        except json.JSONDecodeError:
            # If JSON parsing fails, return raw response
            return {
                "raw_response": response,
                "error": "Failed to parse JSON"
            }
    
    async def analyze_cv_for_job(self, cv_data: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """Analyze CV compatibility with a job offer and suggest improvements"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id=f"cv_analysis_{id(cv_data)}",
            system_message="""Tu es un expert en recrutement. Analyse la compatibilité entre un CV et une offre d'emploi.
            Fournis :
            1. Un score de compatibilité (0-100)
            2. Les points forts du candidat
            3. Les points à améliorer
            4. Des suggestions concrètes pour optimiser le CV
            
            Réponds en JSON."""
        ).with_model("openai", "gpt-5.2")
        
        user_message = UserMessage(
            text=f"""Analyse la compatibilité entre ce profil candidat et cette offre d'emploi :
            
            PROFIL CANDIDAT :
            {json.dumps(cv_data, ensure_ascii=False, indent=2)}
            
            OFFRE D'EMPLOI :
            {job_description}
            
            Format de réponse JSON :
            {{
                "score": 85,
                "points_forts": ["point1", "point2"],
                "points_a_ameliorer": ["point1", "point2"],
                "suggestions": ["suggestion1", "suggestion2"],
                "resume_analyse": "résumé en 2-3 phrases"
            }}"""
        )
        
        response = await chat.send_message(user_message)
        
        import json
        try:
            response_text = response.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif response_text.startswith("```"):
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            analysis = json.loads(response_text)
            return analysis
        except json.JSONDecodeError:
            return {
                "score": 0,
                "raw_response": response,
                "error": "Failed to parse analysis"
            }