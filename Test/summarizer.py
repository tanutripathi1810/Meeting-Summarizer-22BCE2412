from openai import OpenAI
from config import Config


class MeetingSummarizer:
    """Generates meeting summaries and action items using OpenAI API"""
    
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            print("⚠ Warning: OPENAI_API_KEY not set in environment")
            print("  Add your API key to .env file")
        else:
            print("✓ OpenAI API key configured")
        
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        print(f"✓ Using OpenAI model: {self.model}")
    
    def generate_summary(self, transcript):
        """
        Generate a comprehensive meeting summary with action items
        
        Args:
            transcript (str): The meeting transcript text
            
        Returns:
            dict: Dictionary containing summary, key decisions, and action items
        """
        prompt = self._build_summary_prompt(transcript)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert meeting analyst. Your task is to analyze meeting transcripts and extract key information in a structured format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )
            
            summary_text = response.choices[0].message.content
            return self._parse_summary(summary_text)
            
        except Exception as e:
            raise Exception(f"Summary generation failed: {str(e)}")
    
    def _build_summary_prompt(self, transcript):
        """Build the prompt for summary generation"""
        return f"""Analyze the following meeting transcript and provide a comprehensive summary in a professional format.

MEETING TRANSCRIPT:
{transcript}

Please provide your analysis in EXACTLY the following format:

## Summary
[Write a single comprehensive paragraph (3-5 sentences) that captures the main topic, key participants, primary focus areas, and overall objectives. This should be concise but complete, giving someone who didn't attend the meeting a clear understanding of what was discussed and decided.]

## Details
[Provide 2-4 detailed sections breaking down the meeting chronologically or by topic. Each section should:
- Have a clear descriptive title (e.g., "MongoDB Enhancements Overview", "Challenges and Solutions")
- Start with the main speaker's name and what they presented/discussed
- Include specific details, technical points, metrics, dates, or examples mentioned
- Add timestamp references in format (HH:MM:SS) if you can infer timing from context
- Be written as flowing paragraphs (not bullet points)
- Each section should be 3-5 sentences providing depth and context]

Example Detail Section Format:
**Section Title**
[Speaker] presented/discussed/explained [topic], focusing on [key points]. They highlighted that [specific detail or example with dates/metrics if available]. [Additional context about challenges, solutions, or outcomes]. [Any related incidents, impacts, or technical details mentioned] (00:00:00).

## Suggested next steps
[List clear, actionable next steps or action items. If specific people are assigned, mention them. If deadlines are mentioned, include them. Format as bullet points:
- [Action item] - [Assigned to: name if mentioned] - [Due date if mentioned]

If no clear action items were discussed, write: "No suggested next steps were found for this meeting."]

IMPORTANT FORMATTING RULES:
1. Summary section: Single flowing paragraph, no bullet points
2. Details section: Multiple titled subsections with descriptive paragraphs
3. Include specific names, dates, metrics, and technical details from the transcript
4. Use professional, clear language
5. Maintain chronological flow in Details section
6. Make it comprehensive but focused on what matters"""
    
    def _parse_summary(self, summary_text):
        """
        Parse the LLM response into structured format
        
        Args:
            summary_text (str): Raw summary text from LLM
            
        Returns:
            dict: Structured summary data
        """
        sections = {
            'summary': '',
            'details': '',
            'next_steps': [],
            'full_summary': summary_text
        }
        
        try:
            # Split by main sections
            parts = summary_text.split('##')
            
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                
                # Check which section this is
                if part.startswith('Summary'):
                    # Extract everything after "Summary" header
                    content = part.replace('Summary', '', 1).strip()
                    sections['summary'] = content
                    
                elif part.startswith('Details'):
                    # Extract everything after "Details" header
                    content = part.replace('Details', '', 1).strip()
                    sections['details'] = content
                    
                elif part.startswith('Suggested next steps') or part.startswith('Next steps'):
                    # Extract action items as list
                    content = part.replace('Suggested next steps', '', 1).replace('Next steps', '', 1).strip()
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('-'):
                            item = line.lstrip('- ').strip()
                            if item and item != "No suggested next steps were found for this meeting.":
                                sections['next_steps'].append(item)
            
        except Exception as e:
            print(f"Warning: Error parsing summary sections: {str(e)}")
        
        return sections

