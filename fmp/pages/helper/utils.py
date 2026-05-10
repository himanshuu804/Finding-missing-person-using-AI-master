import json
import numpy as np
from PIL import Image
import io


def image_obj_to_numpy(image_obj):
    """Convert a Streamlit uploaded file to a numpy array."""
    image_obj.seek(0)
    img = Image.open(image_obj).convert("RGB")
    return np.array(img)


def extract_face_mesh_landmarks(image_numpy):
    """
    Extract face mesh landmarks using MediaPipe.
    Returns a list of (x, y, z) landmark tuples or empty list if no face found.
    """
    try:
        import mediapipe as mp
        mp_face_mesh = mp.solutions.face_mesh

        with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
        ) as face_mesh:
            results = face_mesh.process(image_numpy)

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark
                return [(lm.x, lm.y, lm.z) for lm in landmarks]
    except Exception as e:
        print(f"Face mesh extraction error: {e}")

    return []


def compare_face_meshes(mesh1_json: str, mesh2_json: str, threshold: float = 0.05) -> float:
    """
    Compare two face meshes stored as JSON strings.
    Returns a similarity score between 0 (different) and 1 (same).
    """
    try:
        m1 = json.loads(mesh1_json)
        m2 = json.loads(mesh2_json)

        if not m1 or not m2:
            return 0.0

        arr1 = np.array(m1)
        arr2 = np.array(m2)

        if arr1.shape != arr2.shape:
            return 0.0

        diff = np.mean(np.linalg.norm(arr1 - arr2, axis=1))
        similarity = max(0.0, 1.0 - (diff / threshold))
        return round(similarity, 4)
    except Exception:
        return 0.0
