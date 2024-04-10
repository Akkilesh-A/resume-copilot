from flask import request,jsonify
from config import app,db
from models import Jobs,AdminLogin

@app.route('/jobs',methods=['GET'])
def get_jobs():
    jobs=Jobs.query.all()
    json_jobs=list(map(lambda job:job.to_json(),jobs))
    return jsonify(json_jobs)

@app.route('/create_job',methods=['POST'])
def create_job():
    job_title=request.json.get("jobTitle")
    tech_stack=request.json.get("techStack")

    if not job_title or not tech_stack:
        return jsonify({"error":"Please provide job title and tech stack"}),400
    
    new_job=Jobs(job_title=job_title,tech_stack=tech_stack)

    try:
        db.session.add(new_job)
        db.session.commit()
    except Exception as e:
        return ({"message":str(e)},400)
    
    return jsonify({"message":"Job Post created successfully"}),201

@app.route('/delete_job/<int:user_id>',methods=['DELETE'])
def delete_job(user_id):
    job=Jobs.query.filter_by(id=user_id).first()

    if not job:
        return jsonify({"message":"Job not found"}),404
    
    db.session.delete(job)
    db.session.commit()

    return jsonify({"message":"Job deleted successfully"}),200


@app.route('/admin_login',methods=['POST'])
def admin_login():
    user_id=request.json.get("userId")
    password=request.json.get("password")
    user_id_from_db=AdminLogin.query.filter_by(user_id=user_id).first()
    password_from_db=AdminLogin.query.filter_by(password=password).first()
    if(user_id_from_db and password_from_db):
        return jsonify({"message":"Login successful"}),200
    else:
        return jsonify({"message":"Login failed"}),401
    
@app.route('/admin_register',methods=['POST'])
def admin_register():
    user_id=request.json.get("userId")
    password=request.json.get("password")
    if not user_id or not password:
        return jsonify({"error":"Please provide user id and password"}),400
    
    new_user=AdminLogin(user_id=user_id,password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return ({"message":str(e)},400)
    
    return jsonify({"message":"Admin registered successfully"}),201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
