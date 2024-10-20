import React, { useState } from 'react';

const FormInput: React.FC = () => {
    const [link, setLink] = useState<string>(''); 

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>): void => { 
        event.preventDefault();
        alert("Your Request has been accepted, soon jobautopilot will help you!");
        setLink('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Enter Link:
                <input
                    type="url"
                    value={link}
                    onChange={(e) => setLink(e.target.value)}
                    required
                />
            </label>
            <button type="submit">Submit</button>
        </form>
    );
};

export default FormInput;
