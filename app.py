import streamlit as st
import os
from SimplerLLM.language.llm import LLM as GenerationLLM, LLMProvider
import re
import json

generation_llm = GenerationLLM.create(provider=LLMProvider.ANTHROPIC, model_name="claude-3-5-sonnet-20240620")

def generate_blog_post(topic, advanced_section, notes, length, tone, audience, focus_keyword):
    prompt = f"""Your task is to write an SEO-optimized blog post based on a given topic, advanced section, and notes.

Your goal is to create an engaging, informative, and well-structured article that is ready for publication and optimized for search engines.

Follow these instructions carefully:

1. Begin by reading the following topic, notes, and focus keyword:

<topic>
{topic}
</topic>

<advanced section>
{advanced_section}
</advanced section>

<notes>
{notes}
</notes>

<focus_keyword>
{focus_keyword}
</focus_keyword>

<parameters>
Length: {length} words
Tone: {tone}
Target Audience: {audience}
</parameters>

1. Structure your blog post according to the following outline, incorporating SEO best practices:
a. SEO-optimized title (include focus keyword near the beginning)
b. Meta description (155-160 characters, including focus keyword)
c. Hook (1-2 sentences)
d. Core Idea and Benefits
e. Implementation Steps
f. Advanced Section
g. Conclusion
h. FAQs to rank as search snippets (incorporate focus keyword naturally)

2. SEO Optimization Guidelines:
    a. Include the focus keyword in:
        - First paragraph (within first 100-150 words)
        - At least one H2 heading
        - Meta description
        - Title
        - URL slug suggestion
        - Image alt text suggestions
    b. Use LSI (Latent Semantic Indexing) keywords and related terms naturally throughout the content
    c. Maintain a keyword density of 1-2% for the focus keyword
    d. Create short, SEO-friendly URLs
    e. Optimize heading structure (H1, H2, H3) with keywords where natural

3. Throughout the blog post:
    a. Suggest diagrams or images to add where they would enhance understanding. Format these as: <image_suggestion>Description of the image|SEO-optimized alt text</image_suggestion>
    b. Propose relevant interlinks to other content within the blog. Format these as: <interlink>Anchor text|Target page</interlink>
    c. Recommend external links to authoritative sources that support your points. Format these as: <external_link>Anchor text|URL</external_link>

4. Writing style and vocabulary:
    a. Adjust your writing style to match the specified tone and target audience
    b. Use vocabulary appropriate for the target audience
    c. Keep sentences and paragraphs clear and concise
    d. Use active voice and conversational tone where appropriate
    e. Explain any technical terms or jargon that cannot be avoided

5. Code snippets and formatting:
   a. When including code snippets, wrap them in appropriate markdown code blocks. Specify the language for syntax highlighting.
   b. Use appropriate HTML tags for headings (h1, h2, h3) and paragraphs (p)
   c. For emphasis, use <strong> for bold and <em> for italics
   d. For lists, use <ul> and <li> tags for unordered lists, and <ol> and <li> for ordered lists

6. Present your final blog post within <blog_post> tags, preceded by the SEO metadata in their own tags:

<seo_metadata>
Title: [SEO-optimized title]
Meta Description: [155-160 character description]
Suggested URL Slug: [SEO-friendly URL]
Focus Keyword: [primary keyword]
Secondary Keywords: [list of LSI keywords used]
</seo_metadata>

<blog_post>
[Your content here]
</blog_post>"""

    return generation_llm.generate_response(prompt=prompt, max_tokens=8096)

def review_blog_post(blog_content, topic, advanced_section, notes, length, tone, audience, focus_keyword):
    prompt = f"""Review the following blog post and check if it adequately covers all the required sections, information, and SEO optimization. Identify any missing or underdeveloped areas based on the original topic, advanced section, notes, and specified parameters.

<original_topic>
{topic}
</original_topic>

<original_advanced_section>
{advanced_section}
</original_advanced_section>

<original_notes>
{notes}
</original_notes>

<focus_keyword>
{focus_keyword}
</focus_keyword>

<parameters>
Length: {length} words
Tone: {tone}
Target Audience: {audience}
</parameters>

<blog_post>
{blog_content}
</blog_post>

Analyze both content quality and SEO optimization. Format your response as a JSON object with the following structure:
{{
    "seo_analysis": {{
        "keyword_presence": {{
            "title": bool,
            "meta_description": bool,
            "first_paragraph": bool,
            "headings": bool,
            "image_alt_text": bool
        }},
        "keyword_density": float,
        "missing_seo_elements": [str],
        "seo_improvements": [str]
    }},
    "content_analysis": {{
        "missing_sections": [str],
        "needs_more_detail": [str],
        "organization_suggestions": [str],
        "other_improvements": [str]
    }},
    "parameter_adjustments": [str]
}}"""

    return generation_llm.generate_response(prompt=prompt, max_tokens=2048)

def final_review(blog_content, review_suggestions, length, tone, audience, focus_keyword):
    prompt = f"""Perform a final review of the blog post based on the previous review suggestions. Make necessary improvements to both content and SEO optimization to ensure the blog post is complete, well-structured, and ready for publication.

<blog_post>
{blog_content}
</blog_post>

<review_suggestions>
{review_suggestions}
</review_suggestions>

<parameters>
Length: {length} words
Tone: {tone}
Target Audience: {audience}
Focus Keyword: {focus_keyword}
</parameters>

Implement the suggested improvements and return the final, polished blog post within <blog_post> tags, preceded by the SEO metadata. Ensure that all SEO elements are properly optimized and the content meets the specified parameters."""

    return generation_llm.generate_response(prompt=prompt, max_tokens=8096)

def extract_blog_post(content):
    match = re.search(r'<blog_post>(.*?)</blog_post>', content, re.DOTALL)
    if match:
        return match.group(1)
    return content  # Return the original content if no match is found

# Initialize session state variables
if 'blog_post' not in st.session_state:
    st.session_state.blog_post = None
if 'review_suggestions' not in st.session_state:
    st.session_state.review_suggestions = None
if 'generation_params' not in st.session_state:
    st.session_state.generation_params = None

# Update the Streamlit UI section
st.title("AI Blog Post Writer")

# Input fields
topic = st.text_input("Enter the blog post topic:")
focus_keyword = st.text_input("Enter the focus keyword for SEO optimization:")
advanced_section = st.text_input("Enter the advanced section topic:")
notes = st.text_area("Enter your notes:")

# Customizable parameters
length = st.select_slider("Blog post length", options=[500, 1000, 1500, 2000, 2500, 3000], value=1500)
tone = st.selectbox("Tone", options=["Professional", "Casual", "Academic", "Humorous"])
audience = st.selectbox("Target Audience", options=["Beginners", "Intermediate", "Advanced", "General"])

# Generate button
if st.button("Generate Blog Post"):
    if topic and notes and focus_keyword:  # Added focus_keyword check
        with st.spinner("Generating blog post..."):
            initial_response = generate_blog_post(topic, advanced_section, notes, length, tone, audience, focus_keyword)
            initial_blog_post = extract_blog_post(initial_response)
            
            review_response = review_blog_post(initial_blog_post, topic, advanced_section, notes, length, tone, audience, focus_keyword)
            
            final_response = final_review(initial_blog_post, review_response, length, tone, audience, focus_keyword)
            final_blog_post = extract_blog_post(final_response)
            
            # Store the generated content and parameters in session state
            st.session_state.blog_post = final_blog_post
            st.session_state.generation_params = {
                "topic": topic,
                "focus_keyword": focus_keyword,
                "advanced_section": advanced_section,
                "notes": notes,
                "length": length,
                "tone": tone,
                "audience": audience
            }
        
        st.success("Blog post generated successfully!")
    else:
        st.error("Please enter a topic, focus keyword, and notes.")

# Display generated content if available
if st.session_state.blog_post:
    st.markdown("## Generated Blog Post")
    st.markdown(st.session_state.blog_post, unsafe_allow_html=True)
    


    

st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Enter the blog post topic in the 'Topic' field.
2. (Optional) Enter an advanced section topic.
3. Enter your notes and any additional information in the 'Notes' field.
4. Adjust the customizable parameters:
   - Blog post length
   - Tone
   - Target Audience
5. Click 'Generate Blog Post' to create your AI-generated blog post.
6. The generated blog post will appear below, with suggested images, interlinks, and external links rendered appropriately.
7. Review suggestions will be displayed to show the improvement process.
8. Provide feedback on the generated blog post to help improve future generations.
""")