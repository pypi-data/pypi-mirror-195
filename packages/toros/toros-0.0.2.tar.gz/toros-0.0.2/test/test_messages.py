import rospy
import torch
import torram

from toros.messages import to_transform_stamped, from_transform_stamped


def test_transform_stamped():
    transl = torch.rand(3)
    aa = torch.rand(3)
    T = torram.geometry.pose_to_transformation_matrix(transl, aa)
    t = rospy.Time(10.31)

    msg = to_transform_stamped(T, t, "source", "target")
    T_, source_frame_id, target_frame_id, t_ = from_transform_stamped(msg)

    assert torch.allclose(T, T_)
    assert source_frame_id == "source"
    assert target_frame_id == "target"
    assert t_ == t
