import { Flex } from '@chakra-ui/layout';
import { RootState } from 'app/store';
import { useAppDispatch, useAppSelector } from 'app/storeHooks';
import IAIIconButton from 'common/components/IAIIconButton';
import { setDoesCanvasNeedScaling } from 'features/canvas/store/canvasSlice';
import CancelButton from 'features/options/components/ProcessButtons/CancelButton';
import InvokeButton from 'features/options/components/ProcessButtons/InvokeButton';
import { setShouldShowOptionsPanel } from 'features/options/store/optionsSlice';
import React from 'react';
import { FaSlidersH } from 'react-icons/fa';

export default function UnifiedCanvasProcessingButtons() {
  const shouldPinOptionsPanel = useAppSelector(
    (state: RootState) => state.options.shouldPinOptionsPanel
  );

  const dispatch = useAppDispatch();

  const handleShowOptionsPanel = () => {
    dispatch(setShouldShowOptionsPanel(true));
    if (shouldPinOptionsPanel) {
      setTimeout(() => dispatch(setDoesCanvasNeedScaling(true)), 400);
    }
  };

  return (
    <Flex flexDirection={'column'} gap="0.5rem">
      <IAIIconButton
        tooltip="Show Options Panel (O)"
        tooltipProps={{ placement: 'top' }}
        aria-label="Show Options Panel"
        onClick={handleShowOptionsPanel}
      >
        <FaSlidersH />
      </IAIIconButton>
      <Flex>
        <InvokeButton iconButton />
      </Flex>
      <Flex>
        <CancelButton width={'100%'} height={'40px'} />
      </Flex>
    </Flex>
  );
}
