import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_job_data(url):
    # Request server to get access
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    ignore_tags = ['script', 'metadata', 'link', 'style', 'svg', 'path']
    
    # Extract job-related data intelligently
    for job_section in soup.find_all('div', class_=['job-card', 'job-listing', 'job-result', 'job']):
        job_title = job_section.find('h2', class_=['job-title', 'title', 'job-heading']).get_text(strip=True) if job_section.find('h2') else None
        company_name = job_section.find('div', class_=['company-name', 'employer', 'company']).get_text(strip=True) if job_section.find('div', class_=['company-name', 'employer', 'company']) else None
        location = job_section.find('span', class_=['location', 'job-location']).get_text(strip=True) if job_section.find('span', class_=['location', 'job-location']) else None
        job_description = job_section.find('p', class_=['description', 'job-summary']).get_text(strip=True) if job_section.find('p', class_=['description', 'job-summary']) else None
        job_link = job_section.find('a', href=True)['href'] if job_section.find('a', href=True) else None

        # Append the structured data for each job listing
        data.append({
            'Job Title': job_title,
            'Company Name': company_name,
            'Location': location,
            'Job Description': job_description,
            'Job Link': job_link
        })

    return pd.DataFrame(data)

def get_form_fields(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    form_data = []
    
    for input_tag in soup.find_all(['input', 'textarea', 'select']):
        field_name = input_tag.get('name', None)
        field_type = input_tag.get('type', None)
        placeholder = input_tag.get('placeholder', None)
        field_id = input_tag.get('id', None)
        
        if field_name:
            form_data.append({
                'Field Name': field_name,
                'Field Type': field_type,
                'Placeholder': placeholder,
                'Field ID': field_id
            })
    
    return pd.DataFrame(form_data)

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    web_address = input("Enter the URL: ")
    
    # Extract job data from the page
    job_data = get_job_data(web_address)
    
    if not job_data.empty:
        save_to_csv(job_data, 'jobListings.csv')
    else:
        print("No job listings found or extracted.")
    
    # Extract form fields from the page for potential auto-filling
    form_data = get_form_fields(web_address)
    
    if not form_data.empty:
        save_to_csv(form_data, 'formFields.csv')
    else:
        print("No form fields found or extracted.")

if __name__ == '__main__':
    main()
