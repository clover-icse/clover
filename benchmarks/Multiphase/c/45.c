int main(){
    int x, y, z;

    // pre-conditions
    x = 0;
    

    // loop body
    while(unknown()){
        if(x >= 765552){
            if(x < 865552){
                y = y + 1;
            }
        }else{
            y = 0;
        }

        if(x >= 663258){
            if(x < 763258){
                z = z + 1;
            }
        }else{
            z = 0;
        }

        x = x + 1;
    }

    // post-condition
    if(x >= 965552){
        assert(y == z);
    }
    
}