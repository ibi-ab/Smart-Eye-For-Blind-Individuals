def poses_to_sentence(poses):
    if ('Neck', 'RShoulder') in poses and ('Neck', 'LShoulder') in poses:
        if ('RShoulder', 'RElbow') in poses and ('LShoulder', 'LElbow') in poses:
            return "The person has raised both arms."
        elif ('RShoulder', 'RElbow') in poses:
            return "The person has raised their right arm."
        elif ('LShoulder', 'LElbow') in poses:
            return "The person has raised their left arm."

    if ('Neck', 'RHip') in poses and ('Neck', 'LHip') in poses:
        if ('RHip', 'RKnee') in poses and ('LHip', 'LKnee') in poses:
            return "The person is standing."

    if ('Neck', 'Nose') in poses:
        return "The person is facing forward."

    if ('Neck', 'RHip') in poses and ('RHip', 'RKnee') in poses and ('RKnee', 'RAnkle') in poses:
        return "The person is kicking with the right leg."

    if ('Neck', 'LHip') in poses and ('LHip', 'LKnee') in poses and ('LKnee', 'LAnkle') in poses:
        return "The person is kicking with the left leg."

    if ('RElbow', 'RWrist') in poses and ('LElbow', 'LWrist') in poses:
        return "The person is waving."

    if ('Neck', 'RHip') in poses and ('RHip', 'RKnee') in poses:
        return "The person is bending their right leg."

    if ('Neck', 'LHip') in poses and ('LHip', 'LKnee') in poses:
        return "The person is bending their left leg."

    if ('RHip', 'RKnee') in poses and ('RKnee', 'RAnkle') in poses:
        return "The person is kicking a ball with their right leg."

    if ('LHip', 'LKnee') in poses and ('LKnee', 'LAnkle') in poses:
        return "The person is kicking a ball with their left leg."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'LShoulder') in poses:
        return "The person has both arms relaxed."

    if ('RShoulder', 'RElbow') in poses and ('LShoulder', 'LElbow') in poses:
        return "The person has both hands."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RHip') in poses and ('Neck', 'RAnkle') in poses:
        return "The person is leaning over to the right."

    if ('Neck', 'LHip') in poses and ('Neck', 'LAnkle') in poses:
        return "The person is leaning over to the left."

    if ('RHip', 'RAnkle') in poses and ('LHip', 'LAnkle') in poses:
        return "The person is sitting on a chair."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is shaking their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is shaking their left hand."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RHip') in poses and ('Neck', 'RAnkle') in poses:
        return "The person is leaning over to the right."

    if ('Neck', 'LHip') in poses and ('Neck', 'LAnkle') in poses:
        return "The person is leaning over to the left."

    if ('RHip', 'RAnkle') in poses and ('LHip', 'LAnkle') in poses:
        return "The person is sitting on a chair."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is shaking their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is shaking their left hand."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RHip') in poses and ('Neck', 'RAnkle') in poses:
        return "The person is leaning over to the right."

    if ('Neck', 'LHip') in poses and ('Neck', 'LAnkle') in poses:
        return "The person is leaning over to the left."

    if ('RHip', 'RAnkle') in poses and ('LHip', 'LAnkle') in poses:
        return "The person is sitting on a chair."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is shaking their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is shaking their left hand."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RHip') in poses and ('Neck', 'RAnkle') in poses:
        return "The person is leaning over to the right."

    if ('Neck', 'LHip') in poses and ('Neck', 'LAnkle') in poses:
        return "The person is leaning over to the left."

    if ('RHip', 'RAnkle') in poses and ('LHip', 'LAnkle') in poses:
        return "The person is sitting on a chair."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is shaking their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is shaking their left hand."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RHip') in poses and ('Neck', 'RAnkle') in poses:
        return "The person is leaning over to the right."

    if ('Neck', 'LHip') in poses and ('Neck', 'LAnkle') in poses:
        return "The person is leaning over to the left."

    if ('RHip', 'RAnkle') in poses and ('LHip', 'LAnkle') in poses:
        return "The person is sitting on a chair."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is shaking their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is shaking their left hand."

    if ('Neck', 'RElbow') in poses and ('Neck', 'RWrist') in poses:
        return "The person is touching their right ear with their right hand."

    if ('Neck', 'LElbow') in poses and ('Neck', 'LWrist') in poses:
        return "The person is touching their left ear with their left hand."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is scratching their right shoulder with their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is scratching their left shoulder with their left hand."

    if ('Neck', 'RHip') in poses and ('Neck', 'RAnkle') in poses:
        return "The person is leaning over to the right."

    if ('Neck', 'LHip') in poses and ('Neck', 'LAnkle') in poses:
        return "The person is leaning over to the left."

    if ('RHip', 'RAnkle') in poses and ('LHip', 'LAnkle') in poses:
        return "The person is sitting on a chair."

    if ('Neck', 'RShoulder') in poses and ('Neck', 'RElbow') in poses:
        return "The person is shaking their right hand."

    if ('Neck', 'LShoulder') in poses and ('Neck', 'LElbow') in poses:
        return "The person is shaking their left hand."

    return "The person's pose is unclear."
