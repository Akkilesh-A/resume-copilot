from config import app, db

class Jobs(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    job_title=db.Column(db.String(100), nullable=False)
    tech_stack=db.Column(db.String(300), nullable=False)

    def to_json(self):
        return {
            "id":self.id,
            "jobTitle":self.job_title,
            "techStack":self.tech_stack
        }
    
class AdminLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(15), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "password": self.password
        }

class JobSeekerResumeScore(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    job_position=db.Column(db.String(100), nullable=False)
    tech_stack=db.Column(db.String(300), nullable=False)
    name=db.Column(db.String(100), nullable=False)
    phone_number=db.Column(db.String(15), nullable=False)

    def to_json(self):
        return {
            "id":self.id,
            "jobPosition":self.job_position,
            "techStack":self.tech_stack,
            "name":self.name,
            "phoneNumber":self.phone_number            
        }
